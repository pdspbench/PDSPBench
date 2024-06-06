package com.kom.dsp.smartgrid;

public class ProcessOutputQ1 {
    
    private long ts;
    private long house;
    private double gal;// GLOBAL AVG LOAD

    public void setTs(long newTs){
        this.ts = newTs;
    }
    public void setHouse(long newHouse){
        this.house = newHouse;
    }
    public void setGal(double newGal){
        this.gal = newGal;
    }
    public long getTs(){
        return this.ts;
    }
    public long getHouse(){
        return this.house;
    }
    public double getGal(){
        return this.gal;
    }

    @Override
    public String toString(){
        return "{'House':"+house+",'GAL':"+gal+"}";
    }
}
