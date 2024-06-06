package com.kom.dsp.LinearRoad;


import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.MapState;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.configuration.Configuration;

import java.util.ArrayList;
import java.util.List;

public class TravelTimeNotificationMapper extends RichMapFunction<VehicleEvent, String> {


    @Override
    public String map(VehicleEvent event) throws Exception {
        if(event.getType()==4){
            ArrayList<Long> vehicleRecordings = Helper.vehicleReports.get(event.getVehicleId());
            if(vehicleRecordings.size()!=0){
                return "VehicleID:"+ event.getVehicleId() + "Time travelled:"+ (vehicleRecordings.get(vehicleRecordings.size()-1) - vehicleRecordings.get(0));

            }else {
                return "VehicleID:"+ event.getVehicleId() + "Time travelled: 0";
            }
        } else {
            return "VehicleID:"+ event.getVehicleId() + "Time travelled: 0";
        }
    }


}
