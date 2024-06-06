package com.kom.dsp.TPCH;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.RichFlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.dropwizard.metrics.DropwizardMeterWrapper;
import org.apache.flink.metrics.Meter;
import org.apache.flink.util.Collector;

public class PriorityMapper implements FlatMapFunction<TPCHEvent, Tuple2<Integer, Integer>> {


    @Override
    public void flatMap(TPCHEvent tpchEvent, Collector<Tuple2<Integer, Integer>> collector) throws Exception {
        collector.collect(new Tuple2<Integer,Integer>(tpchEvent.getOrderPriority(), 1));
    }
}