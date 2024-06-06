package com.kom.dsp.smartgrid;

import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

public class ProcessWindowQ2
        extends ProcessWindowFunction<HouseEvent, ProcessOutputQ2, Tuple3<Long,Long,Long>, TimeWindow> {

    private static final long serialVersionUID = 1L;
    @Override
    public void process(
            Tuple3<Long,Long,Long> id,
            Context ctx,
            Iterable<HouseEvent> readings,
            Collector<ProcessOutputQ2> out)  {

        double avgLoad;
        double totalLoad = 0;
        int cnt = 0;
        for (HouseEvent r : readings) {
            if(r.getHouse() == (Long) id.getField(0)
                    && r.getHouseholds() == (Long) id.getField(1)
                    && r.getPlugs() == (Long) id.getField(2)){
                cnt++;
                totalLoad += r.getValue();
            }
        }

        ProcessOutputQ2 po = new ProcessOutputQ2();
        avgLoad = totalLoad/cnt;
        po.setHouse(id.getField(0));
        po.setHousehold(id.getField(1));
        po.setPlug(id.getField(2));
        po.setLal(avgLoad);
        po.setTs(111111);
        out.collect(po);
    }
}