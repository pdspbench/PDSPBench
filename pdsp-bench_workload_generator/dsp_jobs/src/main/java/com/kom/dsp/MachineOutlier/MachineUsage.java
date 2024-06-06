package com.kom.dsp.MachineOutlier;

public class MachineUsage {

    MachineUsage(String machineId,
                 double timestamp,
                 double cpuUtilPercentage,
                 double memUtilPercentage,
                 double memBW,
                 double missPerThousandInstructions,
                 double netIn,
                 double netOut,
                 double diskIO){
        this.machineId = machineId;
        this.timestamp = timestamp;
        this.cpuUtilPercentage = cpuUtilPercentage;
        this.memUtilPercentage = memUtilPercentage;
        this.memBW = memBW;
        this.missPerThousandInstructions = missPerThousandInstructions;
        this.netIn = netIn;
        this.netOut = netOut;
        this.diskIO = diskIO;
    }
    private String machineId;
    private double timestamp;

    private double cpuUtilPercentage;

    private double memUtilPercentage;

    private double memBW;

    public String getMachineId() {
        return machineId;
    }

    public void setMachineId(String machineId) {
        this.machineId = machineId;
    }

    public double getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(double timestamp) {
        this.timestamp = timestamp;
    }

    public double getCpuUtilPercentage() {
        return cpuUtilPercentage;
    }

    public void setCpuUtilPercentage(double cpuUtilPercentage) {
        this.cpuUtilPercentage = cpuUtilPercentage;
    }

    public double getMemUtilPercentage() {
        return memUtilPercentage;
    }

    public void setMemUtilPercentage(double memUtilPercentage) {
        this.memUtilPercentage = memUtilPercentage;
    }

    public double getMemBW() {
        return memBW;
    }

    public void setMemBW(double memBW) {
        this.memBW = memBW;
    }

    public double getMissPerThousandInstructions() {
        return missPerThousandInstructions;
    }

    public void setMissPerThousandInstructions(long missPerThousandInstructions) {
        this.missPerThousandInstructions = missPerThousandInstructions;
    }

    public double getNetIn() {
        return netIn;
    }

    public void setNetIn(double netIn) {
        this.netIn = netIn;
    }

    public double getNetOut() {
        return netOut;
    }

    public void setNetOut(double netOut) {
        this.netOut = netOut;
    }

    public double getDiskIO() {
        return diskIO;
    }

    public void setDiskIO(double diskIO) {
        this.diskIO = diskIO;
    }

    private double missPerThousandInstructions;

    private double netIn;

    private double netOut;

    private double diskIO;


    // Calculate the Euclidean distance between two MachineUsage objects
    public double getEuclideanDistance(MachineUsage other) {
        double cpuUtilDiff = this.cpuUtilPercentage - other.cpuUtilPercentage;
        double memUtilDiff = this.memUtilPercentage - other.memUtilPercentage;
        double memGpsDiff = this.memBW - other.memBW;
        double mkpiDiff = this.missPerThousandInstructions - other.missPerThousandInstructions;
        double netInDiff = this.netIn - other.netIn;
        double netOutDiff = this.netOut - other.netOut;
        double diskIoDiff = this.diskIO - other.diskIO;

        // Calculate the sum of squared differences
        double sumOfSquaredDifferences = cpuUtilDiff * cpuUtilDiff +
                memUtilDiff * memUtilDiff +
                memGpsDiff * memGpsDiff +
                mkpiDiff * mkpiDiff +
                netInDiff * netInDiff +
                netOutDiff * netOutDiff +
                diskIoDiff * diskIoDiff;

        // Return the square root of the sum of squared differences
        return Math.sqrt(sumOfSquaredDifferences);
    }
}
