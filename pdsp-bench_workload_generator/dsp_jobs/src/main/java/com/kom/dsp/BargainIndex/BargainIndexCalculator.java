package com.kom.dsp.BargainIndex;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.streaming.api.functions.co.RichCoFlatMapFunction;
import org.apache.flink.util.Collector;

public class BargainIndexCalculator implements FlatMapFunction<Tuple4<String, Double, Long, Double>, Tuple3<String, Double, Long>> {

    @Override
    public void flatMap(Tuple4<String, Double, Long, Double> in, Collector<Tuple3<String, Double, Long>> collector) throws Exception {
        if (in.f3 > 0) {
            collector.collect(new Tuple3<>(in.f0, in.f2/in.f3, in.f2));
        } else {
            collector.collect(new Tuple3<>(in.f0, in.f3, in.f2));
        }
    }
}
