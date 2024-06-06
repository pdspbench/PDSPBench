package com.kom.dsp.LogsAnalyzer;

import org.apache.flink.api.common.state.MapState;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.apache.flink.configuration.Configuration;

import java.awt.*;

// Flink process function to count the number of occurrences of each status code
public class StatusCounter extends ProcessWindowFunction<LogEvent, String, String, TimeWindow> {
    private transient MapState<String, Integer> statusCodeCountState;

    @Override
    public void open(Configuration parameters) throws Exception {
        MapStateDescriptor<String, Integer> descriptor = new MapStateDescriptor<>("statusCodeCount", Types.STRING, Types.INT);
        statusCodeCountState = getRuntimeContext().getMapState(descriptor);
    }

    @Override
    public void process(String s, ProcessWindowFunction<LogEvent, String, String, TimeWindow>.Context context, Iterable<LogEvent> iterable, Collector<String> collector) throws Exception {
        // Increment the count for the status code
        for(LogEvent event : iterable) {
            Integer currentCount = statusCodeCountState.get(event.getStatusCode());
            if (currentCount == null) {
                currentCount = 0;
            }
            currentCount++;
            statusCodeCountState.put(event.getStatusCode(), currentCount);

            // Emit the status code and its count as a string
            collector.collect(event.getStatusCode() + ": " + currentCount);
        }
    }
}