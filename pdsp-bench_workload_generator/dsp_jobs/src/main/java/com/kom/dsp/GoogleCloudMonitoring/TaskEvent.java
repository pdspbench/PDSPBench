package com.kom.dsp.GoogleCloudMonitoring;

import java.io.Serializable;

public class TaskEvent implements Serializable {
    public long timestamp;
    public long jobId;
    public long taskId;
    public long machineId;
    public int eventType;
    public int userId;
    public int category;
    public int priority;
    public float cpu;
    public float ram;
    public float disk;
    public int constraints;

    public TaskEvent() {
    }

    public TaskEvent(long timestamp, long jobId, long taskId, long machineId, int eventType, int userId, int category, int priority, float cpu, float ram, float disk, int constraints) {
        this.timestamp = timestamp;
        this.jobId = jobId;
        this.taskId = taskId;
        this.machineId = machineId;
        this.eventType = eventType;
        this.userId = userId;
        this.category = category;
        this.priority = priority;
        this.cpu = cpu;
        this.ram = ram;
        this.disk = disk;
        this.constraints = constraints;
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

    public long getTaskId() {
        return taskId;
    }

    public void setTaskId(long taskId) {
        this.taskId = taskId;
    }

    public long getMachineId() {
        return machineId;
    }

    public void setMachineId(long machineId) {
        this.machineId = machineId;
    }

    public int getEventType() {
        return eventType;
    }

    public void setEventType(int eventType) {
        this.eventType = eventType;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public int getCategory() {
        return category;
    }

    public void setCategory(int category) {
        this.category = category;
    }

    public int getPriority() {
        return priority;
    }

    public void setPriority(int priority) {
        this.priority = priority;
    }

    public float getCpu() {
        return cpu;
    }

    public void setCpu(float cpu) {
        this.cpu = cpu;
    }

    public float getRam() {
        return ram;
    }

    public void setRam(float ram) {
        this.ram = ram;
    }

    public float getDisk() {
        return disk;
    }

    public void setDisk(float disk) {
        this.disk = disk;
    }

    public int getConstraints() {
        return constraints;
    }

    public void setConstraints(int constraints) {
        this.constraints = constraints;
    }

    @Override
    public String toString() {
        return "TaskEvent{" +
                "timestamp=" + timestamp +
                ", jobId=" + jobId +
                ", taskId=" + taskId +
                ", machineId=" + machineId +
                ", eventType=" + eventType +
                ", userId=" + userId +
                ", category=" + category +
                ", priority=" + priority +
                ", cpu=" + cpu +
                ", ram=" + ram +
                ", disk=" + disk +
                ", constraints=" + constraints +
                '}';
    }
}