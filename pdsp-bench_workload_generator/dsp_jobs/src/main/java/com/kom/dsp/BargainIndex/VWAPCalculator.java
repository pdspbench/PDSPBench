package com.kom.dsp.BargainIndex;

import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.functions.windowing.RichWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.apache.flink.streaming.api.windowing.windows.GlobalWindow;
public class VWAPCalculator extends ProcessWindowFunction<QuoteData, Tuple4<String, Double, Long, Double>, String, TimeWindow> {
    @Override
    public void process(String symbol, Context ctx, Iterable<QuoteData> input, Collector<Tuple4<String, Double, Long,Double>> out) {

        double totalPrice = 0.0;
        long totalVolume = 0;
        double quotePrice = 0.0;
        for (QuoteData record : input) {
            totalPrice += record.getClose() * record.getVolume();
            totalVolume += record.getVolume();
            quotePrice = record.getClose();
        }
        double vwap = totalPrice / totalVolume;
        out.collect(new Tuple4<>(symbol, vwap, totalVolume, quotePrice));
    }
}