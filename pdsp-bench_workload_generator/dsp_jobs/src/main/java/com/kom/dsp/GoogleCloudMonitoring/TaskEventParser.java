package com.kom.dsp.GoogleCloudMonitoring;

import org.apache.flink.api.common.functions.MapFunction;

class TaskEventParser implements MapFunction<String, TaskEvent> {
    @Override
    public TaskEvent map(String line) throws Exception {
        String[] values = line.split(",");
        try {
        	 return new TaskEvent(Long.parseLong(values[2]),
                    Long.parseLong(values[0]),
                    Long.parseLong(values[1]),
                    Long.parseLong(values[4]),
                    Integer.parseInt(values[18]),
                   (int) Float.parseFloat(values[15]),
                    Integer.parseInt(values[3]),
                    (int )Float.parseFloat(values[7]),
                    Float.parseFloat(values[8]),
                    Float.parseFloat(values[9]),
                    Float.parseFloat(values[12]),
                    Integer.parseInt(values[17]));
        }
        catch(Exception e) {
        	e.printStackTrace();
        }
        return new TaskEvent();
    }
    
}