package com.kom.dsp.LinearRoad;

public class TollNotification {

    int vehicleId;

    int segment;

    int toll;
    double averageSpeed;
    int numOfVehicles;
    public TollNotification(int vehicleId, int segment, int toll, double averageSpeed, int numOfVehicles) {
        this.vehicleId = vehicleId;
        this.segment = segment;
        this.toll = toll;
        this.averageSpeed = averageSpeed;
        this.numOfVehicles = numOfVehicles;
    }

    public int getVehicleId() {
        return vehicleId;
    }

    public void setVehicleId(int vehicleId) {
        this.vehicleId = vehicleId;
    }

    public int getSegment() {
        return segment;
    }

    public void setSegment(int segment) {
        this.segment = segment;
    }



    public int getToll() {
        return toll;
    }

    public void setToll(int toll) {
        this.toll = toll;
    }

    public String stringFormatter() {

        return "VehicleId: " + vehicleId + " Segment: "+ segment + " Toll: "+ toll;
    }
}
