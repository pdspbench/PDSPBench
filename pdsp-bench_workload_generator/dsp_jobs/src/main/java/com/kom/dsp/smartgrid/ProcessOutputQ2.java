package com.kom.dsp.smartgrid;

public class ProcessOutputQ2 {
    
    private long ts;
    private long plug;
    private long household;
    private long house;
    private double lal;// GLOBAL AVG LOAD

    public void setTs(long newTs){
        this.ts = newTs;
    }
    public void setHouse(long newHouse){
        this.house = newHouse;
    }
    public void setLal(double newLal){
        this.lal = newLal;
    }
    public void setPlug(long newPlug){
        this.plug = newPlug;
    }
    public void setHousehold(long newHousehold){
        this.household = newHousehold;
    }
    public long getTs(){
        return this.ts;
    }
    public long getHouse(){
        return this.house;
    }
    public double getLal(){
        return this.lal;
    }
    public long getPlug(){
        return this.plug;
    }
    public long getHousehold(){
        return this.household;
    }

    @Override
    public String toString(){
        return "{'House'"+house+",'HouseHold'"+household+",'Plug'"+plug+",'LAL':"+lal+"}";
    }
}
