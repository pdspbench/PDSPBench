package com.kom.dsp.ClickAnalytics;

import org.apache.flink.api.common.functions.ReduceFunction;
import org.apache.flink.api.java.tuple.Tuple3;

public class SumReducer implements ReduceFunction<Tuple3<String, Integer, Integer>> {
    @Override
    public Tuple3<String, Integer, Integer> reduce(Tuple3<String, Integer, Integer> value1, Tuple3<String, Integer, Integer> value2) {
        int sumField2 = value1.f1 + value2.f1; // Sum the second fields
        int sumField3 = value1.f2 + value2.f2; // Sum the third fields
        return Tuple3.of(value1.f0, sumField2, sumField3);
    }
}