package com.kom.dsp.LinearRoad;


import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.MapState;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.configuration.Configuration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class DailyExpenditureCalculator extends RichMapFunction<VehicleEvent, String> {
    private static final Logger LOG = LoggerFactory.getLogger(com.kom.dsp.LinearRoad.DailyExpenditureCalculator.class);
    // vehicle-> Events
    private MapState<Integer, List<VehicleEvent>> vehicleEventsState;

    // Segment-> Vehicles
    private MapState<Integer, List<VehicleEvent>> segmentVehiclesState;

    //vehicles -> expenditure

    private MapState<Integer, Long> vehicleTotalExpenditureState;

    @Override
    public void open(Configuration parameters) {

        // Initialize the MapState to store the last four position reports for each vehicle
        MapStateDescriptor<Integer, List<VehicleEvent>> vehicleEventsDescriptor =
                new MapStateDescriptor<>("vehicleEvents", TypeInformation.of(Integer.class), TypeInformation.of(new TypeHint<List<VehicleEvent>>() {}));
        vehicleEventsState = getRuntimeContext().getMapState(vehicleEventsDescriptor);

        // Initialize the MapState to store the vehicles in each segment
        MapStateDescriptor<Integer, List<VehicleEvent>> segmentVehiclesDescriptor =
                new MapStateDescriptor<>("segmentVehicles", TypeInformation.of(Integer.class), TypeInformation.of(new TypeHint<List<VehicleEvent>>() {}));
        segmentVehiclesState = getRuntimeContext().getMapState(segmentVehiclesDescriptor);


        // Initialize the MapState to store the vehicles in each segment
        MapStateDescriptor<Integer,Long> vehicleTotalExpenditureDescriptor =
                new MapStateDescriptor<>("vehicleTotalExpenditure", TypeInformation.of(Integer.class), TypeInformation.of(Long.class));
        vehicleTotalExpenditureState = getRuntimeContext().getMapState(vehicleTotalExpenditureDescriptor);

        Helper.init();

    }

    @Override
    public String map(VehicleEvent event) throws Exception {
        LOG.info(event.toString());

        if(event.getType()==2) {
            try {
                if (vehicleTotalExpenditureState.get(event.vehicleId) == 0 || vehicleTotalExpenditureState.get(event.vehicleId) == null) {
                    return "";
                }
            } catch(NullPointerException e) {
                    return "Vehicle:"+ event.vehicleId+ ",Total Expenditure: 0";
            }
            return "Vehicle:"+ event.vehicleId+ ",Total Expenditure: "+vehicleTotalExpenditureState.get(event.vehicleId);
        } else if(event.getType()==0) {


            int vehicleId = event.vehicleId;
            int segmentId = event.segment;


            List<VehicleEvent> events = vehicleEventsState.get(vehicleId);
            List<VehicleEvent> vehiclesInSegment = segmentVehiclesState.get(segmentId);


            if (events == null) {
                // If there are no previous events for the vehicle, create a list and store the current event
                events = new ArrayList<>();
                events.add(event);
                vehicleEventsState.put(vehicleId, events);
                vehicleTotalExpenditureState.put(vehicleId, 0L);
                return null;
            } else {
                events.add(event);
                // Update the list of events for the vehicle
                vehicleEventsState.put(vehicleId, events);
            }
            // Keep only the last four events for the vehicle
            if (events.size() > 4) {
                events.remove(0);
            }

            //toll calculation and adding it into vehicletotalexpenditure state
            if (vehiclesInSegment == null) {
                vehiclesInSegment = new ArrayList<>();
                vehiclesInSegment.add(event);
                segmentVehiclesState.put(segmentId, vehiclesInSegment);
                vehicleTotalExpenditureState.put(vehicleId, (long) calculateToll(segmentId,1));
                TollNotification tollNotification = new TollNotification(vehicleId, segmentId, calculateToll(segmentId, 1), event.speed, 1);
                return null;
            }
            else {
                boolean vehiclePresent = false;
                //Check if vehicle is not  present in the segment
                for (VehicleEvent v : vehiclesInSegment) {
                    if (event.vehicleId == v.vehicleId) {
                        vehiclePresent = true;
                        break;
                    }
                }
                if (!vehiclePresent) {
                    vehiclesInSegment.add(event);
                    segmentVehiclesState.put(segmentId, vehiclesInSegment);
                    int lastSegmentId = events.get(events.size() - 1).segment;


                    List<VehicleEvent> lastSegmentVehicle = segmentVehiclesState.get(segmentId);

                    // Remove from last segment

                    List<VehicleEvent> toRemove = new ArrayList<>();

                    for (VehicleEvent v : lastSegmentVehicle) {
                        if (event.vehicleId == v.vehicleId) {
                            toRemove.add(v);
                            break;
                        }
                    }

                    lastSegmentVehicle.removeAll(toRemove);
                    segmentVehiclesState.put(lastSegmentId, lastSegmentVehicle);

                    // Calculate the average speed  for the segment
                    double averageSpeed = calculateAverageSpeed(segmentId);

                    int numVehicles = getNumVehicles(segmentId);

                    // Calculate the toll amount
                    long toll = (long)calculateToll(averageSpeed, numVehicles);
                    Long totalToll = vehicleTotalExpenditureState.get(vehicleId);
                    vehicleTotalExpenditureState.put(vehicleId, totalToll+toll);
                    return null;
                }


            }
            return null;
        }
        return null;
    }


    // Helper method to calculate the average speed for a segment
    private double calculateAverageSpeed(int segmentId) throws Exception {
        double sumSpeed = 0.0;

        List<VehicleEvent> vehiclesInSegment = segmentVehiclesState.get(segmentId);

        // Calculate the sum of speeds and count of vehicles in the segment
        for (VehicleEvent event : vehiclesInSegment) {
            sumSpeed += event.speed;

        }

        // Calculate the average speed
        return sumSpeed/vehiclesInSegment.size();
    }

    // Helper method to get the number of vehicles in a segment during the previous timestamp

    private int getNumVehicles(int segmentId) throws Exception {

        ;

        return segmentVehiclesState.get(segmentId).size();
    }

    // Helper method to calculate the toll based on the average speed and number of vehicles
    private int calculateToll(double averageSpeed, int numVehicles) {
        // By default, the toll amount is 2
        int toll = 2;

        // Check if the average speed and number of vehicles meet the conditions for toll assessment
        if (averageSpeed >= 20 ) {
            toll = (int) ((averageSpeed * numVehicles)/3);
        }

        return toll;
    }
}
