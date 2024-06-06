package com.kom.dsp.SentimentAnalysis;

import org.apache.flink.api.common.functions.MapFunction;

class TwitterAnalyser implements MapFunction<Tweet, TweetScored> {
    @Override
    public TweetScored map(Tweet tweet) throws Exception {
        SentimentClassifier classifier = SentimentClassifierFactory.create(SentimentClassifierFactory.BASIC);
        SentimentResult sentimentResult = classifier.classify(tweet.getText());
        return new TweetScored(tweet.getId(), tweet.getTimestamp(),tweet.getText(),  sentimentResult.getSentiment().toString(), sentimentResult.getScore());
        
    }
}