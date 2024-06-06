package com.kom.dsp.ClickAnalytics;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.apache.flink.api.common.functions.MapFunction;


public class ClickLogParser implements MapFunction<String, ClickLog> {
    @Override
    public ClickLog map(String s) throws Exception {
        JsonObject obj = new JsonParser().parse(s).getAsJsonObject();
        String url = obj.get("url").getAsString();
        String ip = obj.get("ip").getAsString();
        String clientKey = obj.get("clientKey").getAsString();

        return new ClickLog(url, ip, clientKey);
    }
}
