package com.kom.dsp.TrafficMonitoring;


import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple5;

public  class FormatterOutput implements MapFunction<Tuple2<Long,Double>, String>{

    @Override
    public String map(Tuple2<Long, Double> stringDoubleTuple2) throws Exception {
        Long roadId = stringDoubleTuple2.f0;
        Double averageSpeed = stringDoubleTuple2.f1;

        return String.format("Road: %s, Average Speed: %.2f",
                roadId, averageSpeed);
    }
}