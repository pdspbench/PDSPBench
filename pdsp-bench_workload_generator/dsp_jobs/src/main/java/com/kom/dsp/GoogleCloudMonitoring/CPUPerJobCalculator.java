package com.kom.dsp.GoogleCloudMonitoring;

import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

class CPUPerJobCalculator extends ProcessWindowFunction<TaskEvent, CPUPerJob, Long, TimeWindow> {

    @Override
    public void process(Long key, Context context, Iterable<TaskEvent> values, Collector<CPUPerJob> out) throws Exception {
        long minTimestamp = Long.MAX_VALUE;
        long jobId = -1L;
        float sum = (float) 0;
        int count = 0;

        for (TaskEvent value : values) {
            if (minTimestamp >= value.getTimestamp()) {
                minTimestamp = value.getTimestamp();
            }
            jobId = value.getJobId();
            sum = sum + value.getCpu();
            count = count + 1;
        }

        CPUPerJob result = new CPUPerJob(
                minTimestamp,
                jobId,
                sum / count);
        out.collect(result);
    }
}
