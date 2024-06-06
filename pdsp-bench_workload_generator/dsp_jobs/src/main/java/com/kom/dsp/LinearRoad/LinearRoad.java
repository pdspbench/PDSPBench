package com.kom.dsp.LinearRoad;


import com.kom.dsp.utils.Constants;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.restartstrategy.RestartStrategies;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.core.execution.JobClient;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.CheckpointConfig;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.util.concurrent.CompletableFuture;

public class LinearRoad {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.getConfig().setLatencyTrackingInterval(10);
        env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);
        // Enable checkpointing and set the checkpoint interval
        env.getConfig().setLatencyTrackingInterval(10);
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
        DataStream<VehicleEvent> source = null;
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
                        .map(new VehicleEventParser())
                        .setParallelism(Integer.parseInt(parallelism_degree[0]))
                        .name("Vehicle-event-parser");

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

        if(query == Constants.QUERY_ONE) {
            DataStream<TollNotification> tollNotificationStream = source
                    .keyBy(event -> event.vehicleId)
                    .map(new TollNotificationMapper())

                    .name("toll-notification")
                    .setParallelism(Integer.parseInt(parallelism_degree[1]));

            DataStream<String> resultStream = tollNotificationStream.map(new TollNotificationFormatter())
                    .filter(value -> value!=null)
                    .name("formatter-toll-notification")
                    .setParallelism(Integer.parseInt(parallelism_degree[2]));


            if (mode.equalsIgnoreCase(Constants.FILE)) {
                resultStream.sinkTo(sink).name("file-sink");
            }
            if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                resultStream.sinkTo(sink).name("kafka-sink");
            }

        }
        else if(query == Constants.QUERY_TWO) {


            DataStream<AccidentNotification> accidentNotificationStream =
                    source.keyBy(value -> value.time)
                    .window(SlidingProcessingTimeWindows.of(Time.seconds(slidingWindowSize), Time.seconds(slidingWindowSlide))) // 5-minute sliding window with 30-second slide
                    .process(new AccidentDetectionProcess())
                    .name("accident-notification")
                    .setParallelism(Integer.parseInt(parallelism_degree[1]));

            DataStream<String> resultStream = accidentNotificationStream.map(new AccidentNotificationFormatter())
                    .filter(value -> value!=null)
                    .name("formatter-accident-notification")
                    .setParallelism(Integer.parseInt(parallelism_degree[2]));


            if (mode.equalsIgnoreCase(Constants.FILE)) {
                resultStream.sinkTo(sink).name("file-sink");
            }
            if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                resultStream.sinkTo(sink).name("kafka-sink");
            }

        }
        else if(query == Constants.QUERY_THREE) {


            DataStream<String> resultStream = source
                    .keyBy(event -> event.vehicleId)
                    .map(new DailyExpenditureCalculator())
                    .name("daily-expenditure")
                    .filter(value-> value != null)
                    .setParallelism(Integer.parseInt(parallelism_degree[1]));




            if (mode.equalsIgnoreCase(Constants.FILE)) {
                resultStream.sinkTo(sink).name("file-sink");
            }
            if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                resultStream.sinkTo(sink).name("kafka-sink");
            }

        }
        else if(query == 4) {

            DataStream<String> resultStream = source
                    .keyBy(event-> event.vehicleId)
                    .map(new VehicleReportsMapper())
                    .name("vehicle-report-mapper")
                    .setParallelism(Integer.parseInt(parallelism_degree[1]));


            if (mode.equalsIgnoreCase(Constants.FILE)) {
                resultStream.sinkTo(sink).name("file-sink");
            }
            if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                resultStream.sinkTo(sink).name("kafka-sink");
            }

        }

        System.out.println("[main] Source and Sink created.");
        env.disableOperatorChaining();

        JobClient client = env.executeAsync("Linear Road");
        System.out.println("Time to cancel activate execution");
        long start = System.currentTimeMillis();
        long end = start + secondsToWait * 1000;
        while (System.currentTimeMillis() < end) {
        }
        CompletableFuture<Void> future=client.cancel();

        System.out.println("Job should be cancelled "+future.isDone());

    }
}


