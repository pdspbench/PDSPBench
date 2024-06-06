package com.kom.dsp.SpikeDetection;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.util.Collector;
import org.joda.time.DateTime;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;
import org.joda.time.format.DateTimeFormatterBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class SensorParser implements FlatMapFunction<String, SensorMeasurement> {

    private static final DateTimeFormatter formatterMillis = new DateTimeFormatterBuilder()
            .appendYear(4, 4).appendLiteral("-").appendMonthOfYear(2).appendLiteral("-")
            .appendDayOfMonth(2).appendLiteral(" ").appendHourOfDay(2).appendLiteral(":")
            .appendMinuteOfHour(2).appendLiteral(":").appendSecondOfMinute(2)
            .appendLiteral(".").appendFractionOfSecond(3, 6).toFormatter();

    private static final DateTimeFormatter formatter = DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss");

    @Override
    public void flatMap(String value, Collector<SensorMeasurement> out) throws Exception {
        String[] fields = value.split("\\s+");
        int count=0;
        for(String field :fields){

            count++;
        }
        	String dateStr = fields[0] + " " +fields[1];
            DateTime date = formatterMillis.parseDateTime("2004-02-28 01:20:16.567523");

            try {
                date = formatterMillis.parseDateTime(dateStr);
            } catch (IllegalArgumentException ex) {
                try {
                    date = formatter.parseDateTime(dateStr);
                } catch (IllegalArgumentException ex2) {
                    System.out.println("Error parsing record date/time field, input record: " + value);
                }
            }

                out.collect(new SensorMeasurement(date.getMillis(),

                        Integer.parseInt(fields[2]),
                        Float.parseFloat(fields[3]),
                        Float.parseFloat(fields[4]),
                        Float.parseFloat(fields[5]),
                        Float.parseFloat(fields[6])));


    }
}
