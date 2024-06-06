package com.kom.dsp.SentimentAnalysis;
import com.kom.dsp.utils.Constants;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.api.common.serialization.SimpleStringEncoder;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.connector.file.sink.FileSink;
import org.apache.flink.connector.file.src.FileSource;
import org.apache.flink.connector.file.src.reader.TextLineFormat;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.core.execution.JobClient;
import org.apache.flink.core.fs.Path;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.sink.filesystem.bucketassigners.BasePathBucketAssigner;
import org.apache.flink.streaming.api.functions.sink.filesystem.rollingpolicies.DefaultRollingPolicy;

import java.time.Duration;
import java.util.concurrent.CompletableFuture;

public class SentimentAnalysis {
    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.getConfig().setLatencyTrackingInterval(10);
        System.out.println("[main] Execution environment created.");

        ParameterTool params = ParameterTool.fromArgs(args);

        String parallelism = params.get("parallelism").replace(" ","").replace("[","").replace("]","").replace("'","");
        String[] parallelism_degree = parallelism.split(",");
        String mode = params.get("mode");
        String input = params.get("input");
        String output = params.get("output");
        String bootstrapServer;
        int watermarkLateness = Integer.parseInt(params.get("lateness"));
        long secondsToWait = Long.parseLong(params.get("waitTimeToCancel"));
        int topicPopularityThreshold = Integer.parseInt(params.get("popularityThreshold"));
        env.setParallelism(Integer.parseInt(parallelism_degree[0]));
        
        DataStream<String> source;
        Sink sink;
        if (mode.equalsIgnoreCase(Constants.FILE)) {
            System.out.println("[main] Arguments parsed.");
            FileSource<String> fileSource = FileSource
                    .forRecordStreamFormat(new TextLineFormat(), new Path(input))
                    .monitorContinuously(Duration.ofSeconds(10))
                    .build();
            source = env.fromSource(fileSource, WatermarkStrategy.noWatermarks(), "file-input");

            sink = FileSink.<TweetScored>forRowFormat(
                            new Path(output), new SimpleStringEncoder<>())
                    .withRollingPolicy(
                            DefaultRollingPolicy.builder()
                                    .withMaxPartSize(20000L)
                                    .withRolloverInterval(1000L)
                                    .build())
                    .withBucketAssigner(new BasePathBucketAssigner<>())
                    .build();
        } else {
            if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                bootstrapServer = params.get("kafka-server");
                System.out.println("[main] Arguments parsed.");
                KafkaSource<String> kafkaSource = KafkaSource.<String>builder()
                        .setBootstrapServers(bootstrapServer)
                        .setTopics(input)
                        .setGroupId("my-group")
                        .setValueOnlyDeserializer(new SimpleStringSchema())
                        .setStartingOffsets(OffsetsInitializer.latest())
                        .build();
                source = env.fromSource(
                                kafkaSource,
                                WatermarkStrategy.noWatermarks(),
                                "kafka-source");

                sink = KafkaSink.<TweetScored>builder()
                        .setBootstrapServers(bootstrapServer)
                        .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                                .setTopic(output)
                                .setValueSerializationSchema((SerializationSchema<TweetScored>) element -> element.toString().getBytes())
                                .build()
                        )
                        .build();
            } else {
                throw new IllegalArgumentException("The only supported modes are \"file\" and \"kafka\".");
            }
        }

        System.out.println("[main] Source and Sink created.");

        DataStream<Tweet> tokens =
                source.map(new TwitterParser()).name("twitter-parser").setParallelism(Integer.parseInt(parallelism_degree[0]));
        System.out.println("[main] Parser created.");

        DataStream<TweetScored> analysis =
                tokens.map(new TwitterAnalyser()).name("twitter-analyser").setParallelism(Integer.parseInt(parallelism_degree[1]));

        System.out.println("[main] Analyser created.");

        if (mode.equalsIgnoreCase(Constants.FILE)) {
            analysis.sinkTo(sink).name("file-sink");
        }
        if (mode.equalsIgnoreCase(Constants.KAFKA)) {
            analysis.sinkTo(sink).name("kafka-sink");
        }

        System.out.println("[main] Analyser sinks.");
        env.disableOperatorChaining();

        JobClient client = env.executeAsync("Sentiment Analysis");
        System.out.println("Time to cancel activate execution");
        long start = System.currentTimeMillis();
        long end = start + secondsToWait * 1000;
        while (System.currentTimeMillis() < end) {
        }
        CompletableFuture<Void> future=client.cancel();

        System.out.println("Job should be cancelled "+future.isDone());
    }
}

