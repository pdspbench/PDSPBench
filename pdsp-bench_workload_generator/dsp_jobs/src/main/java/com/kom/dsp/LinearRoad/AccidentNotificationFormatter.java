package com.kom.dsp.LinearRoad;

import org.apache.flink.api.common.functions.MapFunction;

public class AccidentNotificationFormatter implements MapFunction<AccidentNotification, String> {

    @Override
    public String map(AccidentNotification accidentNotification) throws Exception {

        return accidentNotification.stringFormatter();

    }


}
