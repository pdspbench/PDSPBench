package com.kom.dsp.wordcount;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.RichFlatMapFunction;
import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.dropwizard.metrics.DropwizardMeterWrapper;
import org.apache.flink.metrics.Meter;
import org.apache.flink.util.Collector;

class Splitter extends RichFlatMapFunction<String, Tuple2<String, Integer>> {

    @Override
    public void flatMap(String sentence, Collector<Tuple2<String, Integer>> out) throws Exception {
        for (String word : sentence.split(" ")) {



            out.collect(new Tuple2<String, Integer>(word, 1));

        }


    }
}