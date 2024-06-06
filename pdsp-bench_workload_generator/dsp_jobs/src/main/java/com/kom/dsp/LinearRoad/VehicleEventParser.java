package com.kom.dsp.LinearRoad;

import com.kom.dsp.LogsAnalyzer.LogEvent;
import com.kom.dsp.TrafficMonitoring.TrafficEvent;
import org.apache.flink.api.common.functions.MapFunction;

// Function to parse the log data into LogEvent objects
public class VehicleEventParser implements MapFunction<String, VehicleEvent> {

    @Override
    public VehicleEvent map(String line) throws Exception {
        // Parse the log data and create a LogEvent object
        // You may need to customize this logic based on the log format
        // Example: "54.36.149.41 - - [22/Jan/2019:03:56:14 +0330] "GET /filter/27|13%20%D9%85%DA%AF%D8%A7%D9%BE%DB%8C%DA%A9%D8%B3%D9%84,27|%DA%A9%D9%85%D8%AA%D8%B1%20%D8%A7%D8%B2%205%20%D9%85%DA%AF%D8%A7%D9%BE%DB%8C%DA%A9%D8%B3%D9%84,p53 HTTP/1.1" 200 30577 "-" "Mozilla/5.0 (compatible; AhrefsBot/6.1; +http://ahrefs.com/robot/)" "-"
        String[] fields = line.split(",");
        if (fields.length == 15) {

            int type = Integer.parseInt(fields[0]);
            long time = Long.parseLong(fields[1]);
            int vehicleId = Integer.parseInt(fields[2]);
            int speed = Integer.parseInt(fields[3]);
            int xway = Integer.parseInt(fields[4]);
            int lane = Integer.parseInt(fields[5]);
            int direction = Integer.parseInt(fields[6]);
            int segment = Integer.parseInt(fields[7]);
            int position = Integer.parseInt(fields[8]);
            int qid = Integer.parseInt(fields[9]);
            int sinit = Integer.parseInt(fields[10]);
            int send = Integer.parseInt(fields[11]);
            int dow = Integer.parseInt(fields[12]);
            int tod = Integer.parseInt(fields[13]);
            int day = Integer.parseInt(fields[14]);

            return new VehicleEvent(type, time, vehicleId, speed, xway, lane, direction, segment, position, qid, sinit, send, dow, tod, day);
        } else {
            return new VehicleEvent();
        }
    }
}