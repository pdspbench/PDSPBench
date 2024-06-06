package com.kom.dsp.SentimentAnalysis;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.apache.flink.api.common.functions.MapFunction;

class TwitterParser implements MapFunction<String, Tweet> {
    @Override
    public Tweet map(String s) throws Exception {
        JsonObject obj = new JsonParser().parse(s).getAsJsonObject();
        String id = obj.get("id").getAsString();
        String text = obj.get("text").getAsString();
        String timestamp = obj.get("created_at").getAsString();

        return new Tweet(id, timestamp, text);
    }
}
