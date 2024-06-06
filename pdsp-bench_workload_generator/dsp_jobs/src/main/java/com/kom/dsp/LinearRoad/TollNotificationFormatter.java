package com.kom.dsp.LinearRoad;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;

public class TollNotificationFormatter implements MapFunction<TollNotification, String> {

    @Override
    public String map(TollNotification tollNotification) throws Exception {
        if(tollNotification == null) {

            return null;
        }
        return tollNotification.stringFormatter();

    }

}
