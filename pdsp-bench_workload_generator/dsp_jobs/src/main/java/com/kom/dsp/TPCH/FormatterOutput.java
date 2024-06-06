package com.kom.dsp.TPCH;


import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;

public  class FormatterOutput implements MapFunction<Tuple2<Integer,Integer>, String>{

    @Override
    public String map(Tuple2<Integer, Integer> stringDoubleTuple2) throws Exception {
        // Format the Tuple5 elements into a string representation
        Integer orderPriority = stringDoubleTuple2.f0;
        Integer numberOfOrders = stringDoubleTuple2.f1;

        return "orderPriority : "+ orderPriority + " Number of orders: " + numberOfOrders;
    }
}