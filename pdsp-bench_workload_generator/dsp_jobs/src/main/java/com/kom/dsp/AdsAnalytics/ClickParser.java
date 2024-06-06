package com.kom.dsp.AdsAnalytics;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;

public class ClickParser implements FlatMapFunction<String, AdEvent> {
    @Override
    public void flatMap(String value, Collector<AdEvent> out) throws Exception {
        String[] record = value.split("\t");

        if (record.length == 12) {

            int clicks = Integer.parseInt(record[0]);
            int views = Integer.parseInt(record[1]);
            String displayUrl = record[2];
            long adId = Long.parseLong(record[3]);
            long advertiserId = Long.parseLong(record[4]);
            int depth = Integer.parseInt(record[5]);
            int position = Integer.parseInt(record[6]);
            long queryId = Long.parseLong(record[7]);
            long keywordId = Long.parseLong(record[8]);
            long titleId = Long.parseLong(record[9]);
            long descriptionId = Long.parseLong(record[10]);
            long userId = Long.parseLong(record[11]);

            for (int i = 0; i <  clicks; i++) {
                String type;
                    type = "click";
                    AdEvent event = new AdEvent(type, clicks, views, displayUrl, adId, advertiserId, depth, position, queryId, keywordId, titleId, descriptionId, userId, 1);
                    out.collect(event);
            }
        }
    }
}
