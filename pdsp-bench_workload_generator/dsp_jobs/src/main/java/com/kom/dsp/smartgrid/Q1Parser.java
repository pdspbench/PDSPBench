package com.kom.dsp.smartgrid;


import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;

public class Q1Parser extends ProcessFunction<ProcessOutputQ1, String> {


    @Override
    public void processElement(ProcessOutputQ1 event, Context ctx, Collector<String> out) throws Exception {
        // Increment the count for the status code


        // Emit the status code and its count as a string
        out.collect(event.toString());
    }
}