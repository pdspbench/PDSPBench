package com.kom.dsp.TrafficMonitoring;

public class TrafficEventWithRoad {
    private Long roadId;
    private String vehicleId;
    private double latitude;
    private double longitude;
    private double speed;

    public Long getRoadId() {
        return roadId;
    }

    public void setRoadId(Long roadId) {
        this.roadId = roadId;
    }

    public String getVehicleId() {
        return vehicleId;
    }

    public void setVehicleId(String vehicleId) {
        this.vehicleId = vehicleId;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public double getSpeed() {
        return speed;
    }

    public void setSpeed(double speed) {
        this.speed = speed;
    }

    public TrafficEventWithRoad(String vehicleId, Long roadId, double latitude, double longitude, double speed) {
        this.vehicleId = vehicleId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.speed = speed;
        this.roadId = roadId;

    }

    public TrafficEventWithRoad(){

    }
}
