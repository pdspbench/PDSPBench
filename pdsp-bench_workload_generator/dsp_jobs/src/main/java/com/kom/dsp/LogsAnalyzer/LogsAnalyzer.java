package com.kom.dsp.LogsAnalyzer;

import com.kom.dsp.utils.Constants;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.core.execution.JobClient;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.util.concurrent.CompletableFuture;

public class LogsAnalyzer {
    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.getConfig().setLatencyTrackingInterval(10);
        env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);
        System.out.println("[main] Execution environment created.");

        ParameterTool params = ParameterTool.fromArgs(args);

        String parallelism = params.get("parallelism").replace(" ","").replace("[","").replace("]","").replace("'","");
        String[] parallelism_degree = parallelism.split(",");
        long secondsToWait = Long.parseLong(params.get("waitTimeToCancel"));
        String mode = params.get("mode");
        String input = params.get("input");// Contains LOG_PROCESSINGIN
        String output = params.get("output");
        String bootstrapServer;
        int query = Integer.parseInt(params.get("query"));
        int slidingWindowSize = Integer.parseInt(params.get("size")); // important to implement
        int slidingWindowSlide = Integer.parseInt(params.get("slide"));
        int watermarkLateness = Integer.parseInt(params.get("lateness"));
        int topicPopularityThreshold = Integer.parseInt(params.get("popularityThreshold"));
        env.setParallelism(Integer.parseInt(parallelism_degree[0]));


        DataStream<LogEvent> source = null;
        Sink sink = null;
        if (mode.equalsIgnoreCase(Constants.FILE)) {
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
                        "kafka-source")
                        .map(new LogParser())
                        .setParallelism(Integer.parseInt(parallelism_degree[0]))
                        .name("Log-parser");

                KafkaSink<String> kafkaSink = KafkaSink.<String>builder()
                        .setBootstrapServers(bootstrapServer)
                        .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                                .setTopic(output)
                                .setValueSerializationSchema(new SimpleStringSchema())
                                .build()
                        )
                        .build();
                sink = kafkaSink;
            } else {
                throw new IllegalArgumentException("The only supported modes are \"file\" and \"kafka\".");
            }
        }

        System.out.println("[main] Source and Sink created.");


        // For Volume counter
        if (query == 1) {
            DataStream<String> volumeCounterStream = source
                    .keyBy(value -> value.getLogTime())
                    .window(SlidingProcessingTimeWindows.of(Time.seconds(slidingWindowSize), Time.seconds(slidingWindowSlide)))
                    .process(new VolumeCounter())
                    .setParallelism(Integer.parseInt(parallelism_degree[1]))
                    .name("volume-counter");

            System.out.println("[main] VolumeCounter [Query 1] operator created.");

            if (mode.equalsIgnoreCase(Constants.FILE)) {
                volumeCounterStream.sinkTo(sink).name("file-sink");
            }
            if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                volumeCounterStream.sinkTo(sink).name("kafka-sink");
            }

            System.out.println("[main] VolumeCounter [Query 1] sink created.");

        } else {
            if (query == 2) {
                DataStream<String> statusCounterStream = source
                        .keyBy(value -> value.getLogTime())
                        .window(SlidingProcessingTimeWindows.of(Time.seconds(slidingWindowSize), Time.seconds(slidingWindowSlide)))
                        .process(new StatusCounter())
                        .setParallelism(Integer.parseInt(parallelism_degree[1]))
                        .name("status-counter");

                System.out.println("[main] StatusCounter [Query 2] operator created.");

                if (mode.equalsIgnoreCase(Constants.FILE)) {
                    statusCounterStream.sinkTo(sink).name("file-sink");
                }
                if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                    statusCounterStream.sinkTo(sink).name("kafka-sink");
                }

                System.out.println("[main] StatusCounter [Query 2] sink created.");

            }
        }
        env.disableOperatorChaining();

        JobClient client = env.executeAsync("Logs Processing");
        System.out.println("Time to cancel activate execution");
        long start = System.currentTimeMillis();
        long end = start + secondsToWait * 1000;
        while (System.currentTimeMillis() < end) {
        }
        CompletableFuture<Void> future=client.cancel();

        System.out.println("Job should be cancelled "+future.isDone());
    }
}
