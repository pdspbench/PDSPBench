package com.kom.dsp.LinearRoad;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Helper {

    private static final Logger LOG = LoggerFactory.getLogger(com.kom.dsp.LinearRoad.Helper.class);

    public static Map<Integer,Double> totalTollOfVehicle  = new HashMap<>();

    public static Map<Integer, ArrayList<Long>> vehicleReports  = new HashMap<>();

    public static void init() {

        totalTollOfVehicle = new HashMap<>();
        vehicleReports = new HashMap<>();
    }


}
