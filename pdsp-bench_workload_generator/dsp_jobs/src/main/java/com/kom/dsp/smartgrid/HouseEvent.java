package com.kom.dsp.smartgrid;

import java.io.Serializable;

public class HouseEvent implements Serializable {

    private long index;
    private long change;
    private double value;
    private long property;
    private long plugs;
    private long households;
    private long house;

    public String getToString(){
        return "{index:"+index+
                ",change:"+change+
                ",value:"+value+
                ",property:"+property+
                ",plugs:"+plugs+
                ",households:"+households+
                ",house:"+house+
                "}";
    }
    public void setIndex(long newIndex){
            this.index = newIndex;
    }
    public long getIndex(){
            return this.index;
    }
    public void setChange(long newChange){
            this.change = newChange;
    }
    public long getChange(){
            return this.change;
    }
    public void setValue(double newValue){
            this.value = newValue;
    }
    public double getValue(){
            return this.index;
    }
    public void setProperty(long newProperty){
            this.property = newProperty;
    }
    public long getProperty(){
            return this.property;
    }
    public void setPlugs(long newPlugs){
            this.plugs = newPlugs;
    }
    public long getPlugs(){
            return this.plugs ;
    }
    public void setHouseholds(long newHouseholds){
            this.households = newHouseholds;
    }
    public long getHouseholds(){
            return this.households;
    }
    public void setHouse(long newHouse){
            this.house = newHouse;
    }
    public long getHouse(){
            return this.house;
    }

    public HouseEvent(long index, long change, double value, long property, long plugs, long households, long house) {
        this.index = index;
        this.change = change;
        this.value = value;
        this.property = property;
        this.plugs = plugs;
        this.households = households;
        this.house = house;
    }
}