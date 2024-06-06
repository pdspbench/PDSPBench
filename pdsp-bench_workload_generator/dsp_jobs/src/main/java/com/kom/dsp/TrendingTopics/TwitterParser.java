package com.kom.dsp.TrendingTopics;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.apache.flink.api.common.functions.MapFunction;

class TwitterParser implements MapFunction<String, Tweet> {
    @Override
    public Tweet map(String s) throws Exception {
        String[] values = s.split(",");
        return new Tweet(values[1], values[2], values[5]);
    }
}
