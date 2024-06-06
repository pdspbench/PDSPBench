package com.kom.dsp.LogsAnalyzer;

import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

// Flink process function to count the number of visits per minute
public class VolumeCounter extends ProcessWindowFunction< LogEvent, String, String, TimeWindow> {
    private transient ValueState<Long> visitCountState;

    @Override
    public void open(Configuration parameters) throws Exception {
        ValueStateDescriptor<Long> descriptor = new ValueStateDescriptor<>("visitCount", Types.LONG);
        visitCountState = getRuntimeContext().getState(descriptor);
    }

    @Override
    public void process(String s, ProcessWindowFunction<LogEvent, String, String, TimeWindow>.Context context, Iterable<LogEvent> iterable, Collector<String> collector) throws Exception {
        for(LogEvent event : iterable){
            // Increment the visit count for the minute
            Long currentCount = visitCountState.value();
            if (currentCount == null) {
                currentCount = 0L;
            }
            currentCount++;
            visitCountState.update(currentCount);

            // Emit the time and visit count as a string
            collector.collect(event.getLogTime() + ": " + currentCount);
        }
    }
}
