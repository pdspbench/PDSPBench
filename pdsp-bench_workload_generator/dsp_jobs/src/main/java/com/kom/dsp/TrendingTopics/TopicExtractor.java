package com.kom.dsp.TrendingTopics;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.util.Collector;

public class TopicExtractor implements FlatMapFunction<Tweet, Tuple2<String, Integer>> {
    @Override
    public void flatMap(Tweet tweet, Collector<Tuple2<String, Integer>> out) {
        // Parse the tweet data
        String tweetText = tweet.getText();
        String[] lines = tweetText.split("\n");
        String topic = null;

        for (String line : lines) {

            String[] words = line.split("\\s+");
            for (String word : words) {
                if (word.startsWith("@") || word.startsWith("#")) {
                    topic = word.substring(1);
                    out.collect(new Tuple2<>(topic, 1));
                }
            }


        }
    }
}