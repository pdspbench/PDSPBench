package com.kom.dsp.LinearRoad;


import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.MapState;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.configuration.Configuration;

import java.util.ArrayList;
import java.util.List;

public class VehicleReportsMapper extends RichMapFunction<VehicleEvent, String> {
    // vehicle-> Events
    private MapState<Integer, List<VehicleEvent>> vehicleEventsState;

    @Override
    public void open(Configuration parameters) {

        // Initialize the MapState to store the last four position reports for each vehicle
        MapStateDescriptor<Integer, List<VehicleEvent>> vehicleEventsDescriptor =
                new MapStateDescriptor<>("vehicleEvents", TypeInformation.of(Integer.class), TypeInformation.of(new TypeHint<List<VehicleEvent>>() {
                }));
        vehicleEventsState = getRuntimeContext().getMapState(vehicleEventsDescriptor);


    }

    @Override
    public String map(VehicleEvent event) throws Exception {
        int vehicleId = event.vehicleId;



        List<VehicleEvent> events = vehicleEventsState.get(vehicleId);


        if (events == null) {
            // If there are no previous events for the vehicle, create a list and store the current event
            events = new ArrayList<>();
            events.add(event);
            vehicleEventsState.put(vehicleId, events);


        } else {
            events.add(event);
            // Update the list of events for the vehicle
            vehicleEventsState.put(vehicleId, events);
        }

        if(event.getType() == 4){
            long time_taken = event.getTime() - events.get(0).getTime();
            return "VehicleID: "+vehicleId+ "timeTravelled" + time_taken;
        } else {
            return "VehicleID: "+vehicleId+ "timeTravelled 0";
        }

    }
}
