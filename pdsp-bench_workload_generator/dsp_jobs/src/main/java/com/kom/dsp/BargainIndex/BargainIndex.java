package com.kom.dsp.BargainIndex;


import com.kom.dsp.utils.Constants;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.java.tuple.Tuple4;
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

public class BargainIndex {


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
        String input = params.get("input");
        String output = params.get("output");
        String bootstrapServer;
        int watermarkLateness = Integer.parseInt(params.get("lateness"));
        int topicPopularityThreshold = Integer.parseInt(params.get("popularityThreshold"));
        int slidingWindowSize = Integer.parseInt(params.get("size")); // important to implement
        int slidingWindowSlide = Integer.parseInt(params.get("slide"));
        int windowSize = Integer.parseInt(params.get("size"));

        env.setParallelism(Integer.parseInt(parallelism_degree[0]));


        DataStream<String> source = null;
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
                        "kafka-source");

                sink = KafkaSink.<String>builder()
                        .setBootstrapServers(bootstrapServer)
                        .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                                .setTopic(output)
                                .setValueSerializationSchema(new SimpleStringSchema())
                                .build()
                        )
                        .build();
            } else {
                throw new IllegalArgumentException("The only supported modes are \"file\" and \"kafka\".");
            }
        }

        System.out.println("[main] Source and Sink created.");

        DataStream<QuoteData> parsedQuoteStream =
                source.map(new QuoteDataParser()).name("quote-parser").setParallelism(Integer.parseInt(parallelism_degree[0]));



        DataStream<Tuple4<String, Double, Long, Double>> vwapStream = parsedQuoteStream
                .keyBy(QuoteData::getSymbol)
                .window(SlidingProcessingTimeWindows.of(Time.seconds(slidingWindowSize),Time.seconds(slidingWindowSlide)))
                .process(new VWAPCalculator())
                .name("VWAP-operator")
                .setParallelism(Integer.parseInt(parallelism_degree[1]));
        System.out.println("[main] VWAP operator created.");



        // Calculate bargain index and filter quotes

        DataStream<Tuple3<String, Double, Long>> bargainIndexStream = vwapStream
                .flatMap(new BargainIndexCalculator())
                .name("bargain-index-calculator")
                .setParallelism(Integer.parseInt(parallelism_degree[2]));;
            System.out.println("[main] BargainIndexCalculator operator created.");

            DataStream<String> outputStream = bargainIndexStream.map(new FormatOutputData()).name("output-formatter");

            if (mode.equalsIgnoreCase(Constants.FILE)) {
                outputStream.sinkTo(sink).name("file-sink");
            }
            if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                outputStream.sinkTo(sink).name("kafka-sink");
            }

            System.out.println("[main] sink created.");


        env.disableOperatorChaining();


        JobClient client = env.executeAsync("Bargain Index");
        System.out.println("Time to cancel activate execution");
        long start = System.currentTimeMillis();
        long end = start + secondsToWait * 1000;
        while (System.currentTimeMillis() < end) {
        }
        CompletableFuture<Void> future=client.cancel();

        System.out.println("Job should be cancelled "+future.isDone());
    }
}
