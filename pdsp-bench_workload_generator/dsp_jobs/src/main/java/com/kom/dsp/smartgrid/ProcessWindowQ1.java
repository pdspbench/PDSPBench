package com.kom.dsp.smartgrid;

import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

public class ProcessWindowQ1
        extends ProcessWindowFunction<HouseEvent, ProcessOutputQ1, Long, TimeWindow> {

    private static final long serialVersionUID = 1L;
    @Override
    public void process(Long id,Context ctx,Iterable<HouseEvent> readings,Collector<ProcessOutputQ1> out)  {

        double avgLoad;
        double totalLoad = 0;
        int cnt = 0;
        for (HouseEvent r : readings) {
            if(r.getHouse() == id){
                cnt++;
                totalLoad += r.getValue();
            }

        }
        avgLoad = totalLoad/cnt;

        // get current watermark
        ProcessOutputQ1 po = new ProcessOutputQ1();
        po.setHouse(id);
        po.setGal(avgLoad);
        po.setTs(111111);
        // emit result
        out.collect(po);
    }
}
