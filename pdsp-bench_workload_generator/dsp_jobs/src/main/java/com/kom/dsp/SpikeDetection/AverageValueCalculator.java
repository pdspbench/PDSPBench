package com.kom.dsp.SpikeDetection;

import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AverageValueCalculator extends ProcessWindowFunction<SensorMeasurement, AverageValue, Integer, TimeWindow> {

    private static final Logger LOG = LoggerFactory.getLogger(com.kom.dsp.SpikeDetection.AverageValueCalculator.class);
    @Override
    public void process(Integer key, Context ctx, Iterable<SensorMeasurement> elements, Collector<AverageValue> out) throws Exception {
        int sensorId = -1;
        float currentValue = 0;
        float sum = (float) 0;
        int count = 0;
        

        for (SensorMeasurement element : elements) {
            	
            if(key!= element.getSensorId()) {
                continue;
            }
            
            sum = sum + element.getVoltage();
            count = count + 1;
            currentValue = element.getVoltage();
        }
        LOG.info("Currentvalue"+ currentValue+ " avg: "+(sum/count));
        AverageValue result = new AverageValue(key, currentValue, sum / count);
      
        out.collect(result);
    }
}
