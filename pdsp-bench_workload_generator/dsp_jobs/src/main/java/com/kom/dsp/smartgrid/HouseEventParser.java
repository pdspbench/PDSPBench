package com.kom.dsp.smartgrid;

import com.kom.dsp.LinearRoad.AccidentDetectionProcess;
import org.apache.flink.api.common.functions.MapFunction;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class HouseEventParser implements MapFunction<String, HouseEvent> {

    private static final Logger LOG = LoggerFactory.getLogger(HouseEventParser.class);
    @Override
    public HouseEvent map(String s) throws Exception {
        s = s.replace("\"", "");
        String[] values = s.split(",");
        LOG.info("got "+ values[0]);
        return new HouseEvent(
                Long.parseLong(values[0]),
                Long.parseLong(values[1]),
                Double.parseDouble(values[2]),
                Long.parseLong(values[3]),
                Long.parseLong(values[4]),
                Long.parseLong(values[5]),
                Long.parseLong(values[6]));
    }
}