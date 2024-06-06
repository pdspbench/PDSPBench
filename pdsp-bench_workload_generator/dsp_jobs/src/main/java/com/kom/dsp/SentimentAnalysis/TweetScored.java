package com.kom.dsp.SentimentAnalysis;

import java.io.Serializable;

public class TweetScored implements Serializable {
    public String id;
    public String timestamp;
    public String text;
    public String sentiment;
    public Double sentimentScore;

    public TweetScored(){
    }
    public TweetScored(String id, String timestamp, String text, String sentiment, Double sentimentScore) {
        this.id = id;
        this.timestamp = timestamp;
        this.text = text;
        this.sentiment = sentiment;
        this.sentimentScore = sentimentScore;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getSentiment() {
        return sentiment;
    }

    public void setSentiment(String sentiment) {
        this.sentiment = sentiment;
    }

    public Double getSentimentScore() {
        return sentimentScore;
    }

    public void setSentimentScore(Double sentimentScore) {
        this.sentimentScore = sentimentScore;
    }

    @Override
    public String toString() {
        return "TweetScored{" +
                "id='" + id + '\'' +
                ", timestamp='" + timestamp + '\'' +
                ", text='" + text + '\'' +
                ", sentiment='" + sentiment + '\'' +
                ", sentimentScore=" + sentimentScore +
                '}';
    }
}
