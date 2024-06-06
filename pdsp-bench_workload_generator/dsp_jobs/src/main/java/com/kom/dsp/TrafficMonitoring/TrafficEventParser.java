package com.kom.dsp.TrafficMonitoring;


import org.apache.flink.api.common.functions.MapFunction;
import org.joda.time.DateTime;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;


public class TrafficEventParser implements MapFunction<String, TrafficEvent> {

    private static final SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
    @Override
    public TrafficEvent map(String line) throws ParseException {
        String[] fields = line.split(",");
        if(fields.length == 7){
            String carId  = fields[0];

            String timestamp = fields[2];
            boolean occ   = true;
            double lat    = Double.parseDouble(fields[3]);
            double lon    = Double.parseDouble(fields[4]);
            double speed     = Double.parseDouble(fields[5]);
            double bearing   = Double.parseDouble(fields[6]);
            return new TrafficEvent(carId, timestamp, occ, lat, lon, speed, bearing);
        } else {
            return new TrafficEvent();
        }

    }



}