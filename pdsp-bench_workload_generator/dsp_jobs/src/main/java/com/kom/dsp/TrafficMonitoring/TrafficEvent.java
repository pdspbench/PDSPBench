package com.kom.dsp.TrafficMonitoring;

public class TrafficEvent {
    private String vehicleId;

    private String timestamp;

    private boolean occ;
    private double latitude;
    private double longitude;
    private double speed;

    private double bearing;

    public String getVehicleId() {
        return vehicleId;
    }

    public void setVehicleId(String vehicleId) {
        this.vehicleId = vehicleId;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public boolean isOcc() {
        return occ;
    }

    public void setOcc(boolean occ) {
        this.occ = occ;
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

    public double getBearing() {
        return bearing;
    }

    public void setBearing(double bearing) {
        this.bearing = bearing;
    }

    public TrafficEvent(String vehicleId, String timestamp, boolean occ, double latitude, double longitude, double speed, double bearing) {
        this.vehicleId = vehicleId;
        this.timestamp = timestamp;
        this.occ = occ;
        this.latitude = latitude;
        this.longitude = longitude;
        this.speed = speed;
        this.bearing = bearing;
    }

    public TrafficEvent(){

    }
}
