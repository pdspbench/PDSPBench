package com.kom.dsp.TrafficMonitoring;


import com.esotericsoftware.minlog.Log;
import org.apache.flink.api.common.functions.RichMapFunction;

import org.apache.flink.configuration.Configuration;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Map;


public class RoadMatcher extends RichMapFunction<TrafficEvent, TrafficEventWithRoad> {

    @Override
    public void open(Configuration parameters) throws Exception {
        super.open(parameters);
        Helper.loadShapeFile();

    }

    @Override
    public TrafficEventWithRoad map(TrafficEvent event) throws IOException {
        String vehicleId = event.getVehicleId();
        double latitude = event.getLatitude();
        double longitude = event.getLongitude();

        double speed = event.getSpeed();
        // Retrieve the road_id for the latitude and longitude
        Long roadId = retrieveRoadId(latitude, longitude);

        // Return the taxi_id and road_id as a Tuple2
        return new TrafficEventWithRoad(vehicleId, roadId, latitude, longitude, speed);
    }


    // Retrieve the road ID for the given latitude and longitude
    private static Long retrieveRoadId(double latitude, double longitude) throws IOException {

        DecimalFormat df = new DecimalFormat("#.##");
        latitude = Double.parseDouble(df.format(latitude));
        longitude = Double.parseDouble(df.format(longitude));

        for(Map.Entry<Long,Double[][]> entry : Helper.roadMap.entrySet()){
           Long roadId = entry.getKey();
           Double[][] coordinates = entry.getValue();
           for (Double[] coord : coordinates) {
               if(coord[0].equals(longitude) && coord[1].equals(latitude)) {
                   return roadId;
               }
           }
        }
        return null;
    }
}
