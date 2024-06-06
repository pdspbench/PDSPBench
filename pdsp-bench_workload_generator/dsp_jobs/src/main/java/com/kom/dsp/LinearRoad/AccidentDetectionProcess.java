package com.kom.dsp.LinearRoad;

import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.*;

public class AccidentDetectionProcess extends ProcessWindowFunction<VehicleEvent, AccidentNotification, Long, TimeWindow> {

    private static final Logger LOG = LoggerFactory.getLogger(AccidentDetectionProcess.class);
    @Override
    public void process(Long timestamp, ProcessWindowFunction<VehicleEvent,AccidentNotification,Long,TimeWindow>.Context context,Iterable<VehicleEvent> elements,Collector<AccidentNotification> out) throws Exception {
        LOG.info("Processing window for key: {}", timestamp);
        List<VehicleEvent> listOfVehicles = new ArrayList<VehicleEvent>();
        for (VehicleEvent event : elements) {


            if(event.segment==-1){
                continue;
            }
            listOfVehicles.add(event);

        }
        LOG.info("sagas all: {}", listOfVehicles.size());
        List<VehicleEvent> vehiclesInvolved = findAccidents(listOfVehicles);
                // Emit an accident notification
        if(vehiclesInvolved.size()>0){
            VehicleEvent v = vehiclesInvolved.get(0);
            AccidentNotification accidentNotification = new AccidentNotification(

                    v.lane,
                    v.position,
                    v.time,
                    v.segment
            );
            out.collect(accidentNotification);
        }



    }
    public List<VehicleEvent>  findAccidents(List<VehicleEvent> vehicleEvents) {
        List<VehicleEvent> vehiclesInvolvedInAccident = new ArrayList<>();
        HashSet<String> uniquePositions = new HashSet<>();

        for (VehicleEvent event : vehicleEvents) {
            String key = event.segment + "-" + event.lane + "-" + event.position;

            if (uniquePositions.contains(key)) {
                // Add the vehicle to the result list if it has a duplicate segment, lane, and position
                vehiclesInvolvedInAccident.add(event);
            } else {
                uniquePositions.add(key);
            }
        }

        return vehiclesInvolvedInAccident;
    }

}
