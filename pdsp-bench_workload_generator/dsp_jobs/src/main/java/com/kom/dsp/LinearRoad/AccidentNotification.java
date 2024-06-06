package com.kom.dsp.LinearRoad;
public class AccidentNotification {
    public int lane;

    public int position;

    public long timestamp;
    public int segment;

    public AccidentNotification(int xway, int position, long timestamp, int segment) {
        this.lane = xway;
        this.position = position;
        this.timestamp = timestamp;
        this.segment = segment;
    }

    public int getLane() {
        return lane;
    }

    public void setLane(int lane) {
        this.lane = lane;
    }

    public int getPosition() {
        return position;
    }

    public void setPosition(int position) {
        this.position = position;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public int getSegment() {
        return segment;
    }

    public void setSegment(int segment) {
        this.segment = segment;
    }

    public String stringFormatter() {
        return "Accident occurred at ---"+ "Segment:" + segment + " lane: "+ lane + " position: "+ position + " timestamp: "+ timestamp;
    }
}