package com.kom.dsp.GoogleCloudMonitoring;

import java.io.Serializable;

public class CPUPerJob implements Serializable {
    public long timestamp;
    public long jobId;
    public float averageCpu;

    public CPUPerJob() {
    }

    public CPUPerJob(long timestamp, long jobId, float averageCpu) {
        this.timestamp = timestamp;
        this.jobId = jobId;
        this.averageCpu = averageCpu;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public long getJobId() {
        return jobId;
    }

    public void setJobId(long jobId) {
        this.jobId = jobId;
    }

    public float getAverageCpu() {
        return averageCpu;
    }

    public void setAverageCpu(float averageCpu) {
        this.averageCpu = averageCpu;
    }

    @Override
    public String toString() {
        return "CPUPerJob{" +
                "timestamp=" + timestamp +
                ", jobId=" + jobId +
                ", averageCpu=" + averageCpu +
                '}';
    }
}
