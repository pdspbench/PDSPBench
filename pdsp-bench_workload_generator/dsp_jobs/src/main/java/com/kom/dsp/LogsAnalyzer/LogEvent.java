package com.kom.dsp.LogsAnalyzer;
// POJO class to hold log event data
public class LogEvent {
    private String logTime;
    private String statusCode;

    public LogEvent(String logTime, String statusCode) {
        this.logTime = logTime;
        this.statusCode = statusCode;
    }

    public String getLogTime() {
        return logTime;
    }

    public String getStatusCode() {
        return statusCode;
    }
}

