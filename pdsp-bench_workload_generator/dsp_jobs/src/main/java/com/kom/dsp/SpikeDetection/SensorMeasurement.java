package com.kom.dsp.SpikeDetection;

import java.io.Serializable;

public class SensorMeasurement implements Serializable {
    public long timestamp;

    public int sensorId;
    public float temperature;
    public float humidity;
    public float light;
    public float voltage;

    public SensorMeasurement() {
    }

    public SensorMeasurement(long timestamp, int sensorId, float temperature, float humidity, float light, float voltage) {
        this.timestamp = timestamp;
        this.sensorId = sensorId;
        this.temperature = temperature;
        this.humidity = humidity;
        this.light = light;
        this.voltage = voltage;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public int getSensorId() {
        return sensorId;
    }

    public void setSensorId(int sensorId) {
        this.sensorId = sensorId;
    }

    public float getTemperature() {
        return temperature;
    }

    public void setTemperature(float temperature) {
        this.temperature = temperature;
    }

    public float getHumidity() {
        return humidity;
    }

    public void setHumidity(float humidity) {
        this.humidity = humidity;
    }

    public float getLight() {
        return light;
    }

    public void setLight(float light) {
        this.light = light;
    }

    public float getVoltage() {
        return voltage;
    }

    public void setVoltage(float voltage) {
        this.voltage = voltage;
    }

    @Override
    public String toString() {
        return "SensorMeasurement{" +
                "timestamp=" + timestamp +

                ", sensorId=" + sensorId +
                ", temperature=" + temperature +
                ", humidity=" + humidity +
                ", light=" + light +
                ", voltage=" + voltage +
                '}';
    }
}
