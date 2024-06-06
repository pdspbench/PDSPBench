package com.kom.dsp.MachineOutlier;



import org.apache.flink.api.common.functions.MapFunction;

public class MachineUsageParser implements MapFunction<String, MachineUsage> {
    @Override
    public MachineUsage map(String s) throws Exception {
        String[] values = s.split(",");
        if(values[4].isEmpty() && values[5].isEmpty()){
            return new MachineUsage(values[0],
                    Double.parseDouble(values[1]),
                    Double.parseDouble(values[2]),
                    Double.parseDouble(values[3]),
                    0,
                    0,
                    Double.parseDouble(values[6]),
                    Double.parseDouble(values[7]),
                    Double.parseDouble(values[8]));

        }
        return new MachineUsage(values[0],
                Double.parseDouble(values[1]),
                Double.parseDouble(values[2]),
                Double.parseDouble(values[3]),
                Double.parseDouble(values[4]),
                Double.parseDouble(values[5]),
                Double.parseDouble(values[6]),
                Double.parseDouble(values[7]),
                Double.parseDouble(values[8]));
    }
}