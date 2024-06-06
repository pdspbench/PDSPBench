package com.kom.dsp.SentimentAnalysis;

public interface SentimentClassifier {
    public void initialize();
    public SentimentResult classify(String str);
}
