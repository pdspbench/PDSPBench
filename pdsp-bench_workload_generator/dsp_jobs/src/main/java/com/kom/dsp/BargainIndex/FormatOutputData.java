package com.kom.dsp.BargainIndex;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple3;

public  class FormatOutputData implements MapFunction<Tuple3<String, Double, Long>, String> {
    @Override
    public String map(Tuple3<String, Double, Long> record) {
        return record.f0 + "," + record.f1 + "," + record.f2;
    }
}