package com.kom.dsp.TPCH;

import com.kom.dsp.LinearRoad.AccidentDetectionProcess;
import com.kom.dsp.TrafficMonitoring.TrafficEventWithRoad;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FilterCalculator extends ProcessWindowFunction<TPCHEvent, TPCHEvent, Double, TimeWindow> {
    private static final Logger LOG = LoggerFactory.getLogger(FilterCalculator.class);
    @Override
    public void process(Double aDouble, Context context, Iterable<TPCHEvent> iterable, Collector<TPCHEvent> collector) throws Exception {
        for(TPCHEvent e: iterable){
            LOG.info("OP is "+e.getOrderPriority());
            if(e.getOrderPriority()>2){
                collector.collect(e);
            }
        }
    }
}