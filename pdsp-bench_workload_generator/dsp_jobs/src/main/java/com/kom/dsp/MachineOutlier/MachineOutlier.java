package com.kom.dsp.MachineOutlier;

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
import java.util.List;
import java.util.concurrent.CompletableFuture;

public class MachineOutlier {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        System.out.println("[main] Execution environment created.");
        env.getConfig().setLatencyTrackingInterval(10);
        env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);

        ParameterTool params = ParameterTool.fromArgs(args);

        String parallelism = params.get("parallelism").replace(" ","").replace("[","").replace("]","").replace("'","");
        String[] parallelism_degree = parallelism.split(",");
        String mode = params.get("mode");
        String input = params.get("input");
        String output = params.get("output");
        int query = Integer.parseInt(params.get("query"));
        int slidingWindowSize = Integer.parseInt(params.get("size"));
        int slidingWindowSlide = Integer.parseInt(params.get("slide"));
        double threshold = Double.parseDouble(params.get("popularityThreshold"));
        String bootstrapServer;
        long secondsToWait = Long.parseLong(params.get("waitTimeToCancel"));
        env.setParallelism(Integer.parseInt(parallelism_degree[0]));


        DataStream<String> source = null;
        Sink sink = null;
        if (mode.equalsIgnoreCase(Constants.FILE)) {
            System.out.println("[main] Arguments parsed.");

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
        if(query == Constants.QUERY_ONE) {
            DataStream<MachineUsage> machineUsage =
                    source.map(new MachineUsageParser()).name("machine-usage-parser").setParallelism(Integer.parseInt(parallelism_degree[0]));
            System.out.println("[main] Parser created.");


            DataStream<String> outlierStream = machineUsage
                    .keyBy(MachineUsage::getMachineId)
                    .window(SlidingProcessingTimeWindows.of(Time.seconds(slidingWindowSize), Time.seconds(slidingWindowSlide)))
                    .process(new MachineOutlierWindowFunction())
                    .name("outlier-detector")
                    .setParallelism(Integer.parseInt(parallelism_degree[1]));

            System.out.println("[main] Analyser created.");

            if (mode.equalsIgnoreCase(Constants.FILE)) {
                outlierStream.sinkTo(sink).name("file-sink");
            }
            if (mode.equalsIgnoreCase(Constants.KAFKA)) {
                outlierStream.sinkTo(sink).name("kafka-sink");
            }

            System.out.println("[main] Analyser sinks.");
        }
        env.disableOperatorChaining();

        JobClient client = env.executeAsync("Machine Outlier");
        System.out.println("Time to cancel activate execution");
        long start = System.currentTimeMillis();
        long end = start + secondsToWait * 1000;
        while (System.currentTimeMillis() < end) {
        }
        CompletableFuture<Void> future=client.cancel();

        System.out.println("Job should be cancelled "+future.isDone());
    }
}
