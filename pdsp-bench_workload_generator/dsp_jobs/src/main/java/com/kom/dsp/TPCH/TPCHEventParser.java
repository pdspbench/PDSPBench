package com.kom.dsp.TPCH;


import com.kom.dsp.TrafficMonitoring.TrafficEvent;
import org.apache.flink.api.common.functions.MapFunction;

import java.text.ParseException;
import java.text.SimpleDateFormat;


public class TPCHEventParser implements MapFunction<String, TPCHEvent> {

    @Override
    public TPCHEvent map(String line) throws ParseException {
        String[] fields = line.split(",");
        if(fields.length == 6){
            String orderKey  = fields[0];

            String cname = fields[1];
            String caddress = fields[2];
            int orderPriority     = Integer.parseInt(fields[3]);
            double extendedPrice   = Double.parseDouble(fields[4]);
            double discount   = Double.parseDouble(fields[5]);
            return new TPCHEvent(orderKey, cname, caddress, orderPriority, extendedPrice, discount);
        } else {
            return new TPCHEvent();
        }

    }



}