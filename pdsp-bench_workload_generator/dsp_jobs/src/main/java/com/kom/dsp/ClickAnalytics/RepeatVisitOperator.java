package com.kom.dsp.ClickAnalytics;

import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.util.HashMap;
import java.util.Map;
import org.apache.flink.configuration.Configuration;

// Custom process function to track repeat visits
class RepeatVisitOperator extends ProcessWindowFunction<ClickLog, Tuple3<String,Integer,Integer>, String, TimeWindow> {
    private transient Map<Tuple2<String, String>, Boolean> visitTracker;

    @Override
    public void open(Configuration parameters) throws Exception {
        visitTracker = new HashMap<>();
    }




    @Override
    public void process(String s, ProcessWindowFunction<ClickLog, Tuple3<String, Integer, Integer>, String, TimeWindow>.Context context, Iterable<ClickLog> iterable, Collector<Tuple3<String, Integer, Integer>> collector) throws Exception {
        for(ClickLog event : iterable){
            Tuple2<String, String> key = Tuple2.of(event.getUrl(), event.getClientKey());
            boolean visited = visitTracker.getOrDefault(key, false);
            if (!visited) {
                visitTracker.put(key, true);
                // A new data stream is created of tuple3 which contains URL, total visit counter and Unique visit counter.
                collector.collect(Tuple3.of(event.getUrl(), 1, 1));
            } else {
                collector.collect(Tuple3.of(event.getUrl(), 1, 0));
            }
        }
    }
}
