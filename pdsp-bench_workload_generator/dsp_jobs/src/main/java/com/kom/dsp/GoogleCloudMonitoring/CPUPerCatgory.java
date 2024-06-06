package com.kom.dsp.GoogleCloudMonitoring;

import java.io.Serializable;

public class CPUPerCatgory implements Serializable {
    public long timestamp;
    public int category;
    public float totalCpu;

    public CPUPerCatgory(){
    }

    public CPUPerCatgory(long timestamp, int category, float totalCpu) {
        this.timestamp = timestamp;
        this.category = category;
        this.totalCpu = totalCpu;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public int getCategory() {
        return category;
    }

    public void setCategory(int category) {
        this.category = category;
    }

    public float getTotalCpu() {
        return totalCpu;
    }

    public void setTotalCpu(float totalCpu) {
        this.totalCpu = totalCpu;
    }

    @Override
    public String toString() {
        return "CPUPerCatgory{" +
                "timestamp=" + timestamp +
                ", category=" + category +
                ", totalCpu=" + totalCpu +
                '}';
    }
}
