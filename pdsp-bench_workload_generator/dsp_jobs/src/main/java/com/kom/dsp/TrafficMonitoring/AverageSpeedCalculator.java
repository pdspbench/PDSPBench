package com.kom.dsp.TrafficMonitoring;

import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

public class AverageSpeedCalculator extends ProcessWindowFunction<TrafficEventWithRoad, Tuple2<Long, Double>, Long, TimeWindow> {
    @Override
    public void process(Long key, ProcessWindowFunction<TrafficEventWithRoad, Tuple2<Long, Double>, Long, TimeWindow>.Context context, Iterable<TrafficEventWithRoad> elements, Collector<Tuple2<Long, Double>> out) {
        long count = 0;
        double totalSpeed = 0.0;

        for (TrafficEventWithRoad data : elements) {
            count++;
            totalSpeed += data.getSpeed();
        }

        double avgSpeed = totalSpeed / count;

        out.collect(new Tuple2<>(key, avgSpeed));
    }
}