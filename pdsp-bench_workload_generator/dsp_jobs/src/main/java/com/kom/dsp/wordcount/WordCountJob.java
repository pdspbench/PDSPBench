package com.kom.dsp.wordcount;

import com.kom.dsp.utils.Constants;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.api.common.serialization.SimpleStringEncoder;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.configuration.MemorySize;
import org.apache.flink.connector.file.sink.FileSink;
import org.apache.flink.connector.file.src.FileSource;
import org.apache.flink.connector.file.src.reader.TextLineInputFormat;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.core.execution.JobClient;
import org.apache.flink.core.fs.Path;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.sink.filesystem.bucketassigners.BasePathBucketAssigner;
import org.apache.flink.streaming.api.functions.sink.filesystem.rollingpolicies.DefaultRollingPolicy;

import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;
import org.apache.flink.metrics.Histogram;
import org.apache.flink.metrics.MetricGroup;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * Skeleton for a Flink Word Count data stream Job.
 *
 * <p>To package your application into a JAR file for execution, run
 * 'mvn clean package' on the command line.
 *
 * <p>If you change the name of the main class (with the public static void main(String[] args))
 * method, change the respective entry in the POM.xml file (simply search for 'mainClass').
 */
public class WordCountJob {


	public static void main(String[] args) throws Exception {
		// Sets up the execution environment, which is the main entry point
		// to building Flink applications.
		final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
		env.getConfig().setLatencyTrackingInterval(10);
		env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);
		//ParameterTool is a Flink Class to easily read CLI Arguments

		ParameterTool params = ParameterTool.fromArgs(args);

		// Command line parameters
		String parallelism = params.get("parallelism").replace(" ","").replace("[","").replace("]","").replace("'","");
		String[] parallelism_degree = parallelism.split(",");

		int query = Integer.parseInt(params.get("query"));
		String mode = params.get("mode");
		String input = params.get("input");
		String output = params.get("output");
		long secondsToWait = Long.parseLong(params.get("waitTimeToCancel"));
		int slidingWindowSize = Integer.parseInt(params.get("size"));
		int slidingWindowSlide = Integer.parseInt(params.get("slide"));
		int watermarkLateness = Integer.parseInt(params.get("lateness"));
		int topicPopularityThreshold = Integer.parseInt(params.get("popularityThreshold"));
		env.setParallelism(Integer.parseInt(parallelism_degree[0]));

		String bootstrapServer ;

		DataStream<String> source = null;
		FileSink<Tuple2<String, Integer>> fileSink = null;
		KafkaSink<Tuple2<String, Integer>> kafkaSink = null;

		// Input Mode
		if(mode.equalsIgnoreCase(Constants.KAFKA)){
			bootstrapServer = params.get("kafka-server");
			System.out.println("[main] Arguments parsed.");


			// kafkasource instance receives events in form of string.
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

			kafkaSink = KafkaSink.<Tuple2<String, Integer>>builder()
					.setBootstrapServers(bootstrapServer)
					.setRecordSerializer(KafkaRecordSerializationSchema.builder()
							.setTopic(output)
							.setValueSerializationSchema((SerializationSchema<Tuple2<String, Integer>>) element -> element.toString().getBytes(StandardCharsets.UTF_8))
							.build()
					)
					.build();
		}
		else if(mode.equalsIgnoreCase(Constants.FILE)) {
			System.out.println("File mode selected");
			FileSource<String> fileSource = FileSource
					.forRecordStreamFormat(new TextLineInputFormat(), new Path(input))
					.monitorContinuously(Duration.ofSeconds(10))
					.build();
			source = env.fromSource(fileSource, WatermarkStrategy.noWatermarks(), "file-input");

			fileSink = FileSink.<Tuple2<String, Integer>>forRowFormat(
							new Path(output), new SimpleStringEncoder<>())
					.withRollingPolicy(
							DefaultRollingPolicy
									.builder()
									.withRolloverInterval(Duration.ofMillis(1000L))
									.withMaxPartSize(new MemorySize(1024))
									.build())
					.withBucketAssigner(new BasePathBucketAssigner<>())
					.build();
		}

		// Query Selector
		if(query == Constants.QUERY_ONE){

			assert source != null;
			DataStream<Tuple2<String, Integer>> tokens =
					source.flatMap(new Splitter()).setParallelism(Integer.parseInt(parallelism_degree[0])).name("tokenizer");

			System.out.println("[main] Tokenizer created.");

			DataStream<Tuple2<String, Integer>> counter =
					tokens.keyBy(value -> value.f0).sum(1).setParallelism(Integer.parseInt(parallelism_degree[1])).name("counter");

			System.out.println("[main] Counter created.");
			// Output Mode
			if (mode.equalsIgnoreCase(Constants.FILE)) {
				counter.sinkTo(fileSink).name("file-sink");
			}

			if (mode.equalsIgnoreCase(Constants.KAFKA)) {
				counter.sinkTo(kafkaSink).name("kafka-sink");

			}

		}
		env.disableOperatorChaining();
		JobClient client = env.executeAsync("Flink word count job");
		System.out.println("Time to cancel activate execution");
		long start = System.currentTimeMillis();
		long end = start + secondsToWait * 1000;
		while (System.currentTimeMillis() < end) {
		}
		CompletableFuture<Void> future=client.cancel();

		System.out.println("Job should be cancelled "+future.isDone());

	}
}
