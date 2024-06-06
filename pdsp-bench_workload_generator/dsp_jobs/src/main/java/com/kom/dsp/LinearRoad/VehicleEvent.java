package com.kom.dsp.LinearRoad;

public class VehicleEvent {
    public int type;
    public long time;
    public int vehicleId;
    public int speed;
    public int xway;
    public int lane;
    public int direction;
    public int segment;

    public int position;
    public int qid;
    public int sinit;
    public int send;
    public int dow;
    public int tod;
    public int day;

    public VehicleEvent(int type, long time, int vehicleId, int speed, int xway, int lane, int direction, int segment, int position, int qid, int sinit, int send, int dow, int tod, int day) {
        this.type = type;
        this.time = time;
        this.vehicleId = vehicleId;
        this.speed = speed;
        this.xway = xway;
        this.lane = lane;
        this.direction = direction;
        this.segment = segment;
        this.position = position;
        this.qid = qid;
        this.sinit = sinit;
        this.send = send;
        this.dow = dow;
        this.tod = tod;
        this.day = day;
    }

    public VehicleEvent(){
        super();
    }

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }

    public long getTime() {
        return time;
    }

    public void setTime(long time) {
        this.time = time;
    }

    public int getVehicleId() {
        return vehicleId;
    }

    public void setVehicleId(int vehicleId) {
        this.vehicleId = vehicleId;
    }

    public int getSpeed() {
        return speed;
    }

    public void setSpeed(int speed) {
        this.speed = speed;
    }

    public int getXway() {
        return xway;
    }

    public void setXway(int xway) {
        this.xway = xway;
    }

    public int getLane() {
        return lane;
    }

    public void setLane(int lane) {
        this.lane = lane;
    }

    public int getDirection() {
        return direction;
    }

    public void setDirection(int direction) {
        this.direction = direction;
    }

    public int getSegment() {
        return segment;
    }

    public void setSegment(int segment) {
        this.segment = segment;
    }

    public int getPosition() {
        return position;
    }

    public void setPosition(int position) {
        this.position = position;
    }

    public int getQid() {
        return qid;
    }

    public void setQid(int qid) {
        this.qid = qid;
    }

    public int getSinit() {
        return sinit;
    }

    public void setSinit(int sinit) {
        this.sinit = sinit;
    }

    public int getSend() {
        return send;
    }

    public void setSend(int send) {
        this.send = send;
    }

    public int getDow() {
        return dow;
    }

    public void setDow(int dow) {
        this.dow = dow;
    }

    public int getTod() {
        return tod;
    }

    public void setTod(int tod) {
        this.tod = tod;
    }

    public int getDay() {
        return day;
    }

    public void setDay(int day) {
        this.day = day;
    }

    @Override
    public String toString() {
        return "VehicleEvent{" +
                "type=" + type +
                ", time=" + time +
                ", vehicleId=" + vehicleId +
                ", speed=" + speed +
                ", xway=" + xway +
                ", lane=" + lane +
                ", direction=" + direction +
                ", segment=" + segment +
                ", position=" + position +
                ", qid=" + qid +
                ", sinit=" + sinit +
                ", send=" + send +
                ", dow=" + dow +
                ", tod=" + tod +
                ", day=" + day +
                '}';
    }
}
