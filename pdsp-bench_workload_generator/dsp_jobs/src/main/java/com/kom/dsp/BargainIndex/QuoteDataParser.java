package com.kom.dsp.BargainIndex;

import org.apache.flink.api.common.functions.MapFunction;

public class QuoteDataParser implements MapFunction<String, QuoteData> {
    @Override
    public QuoteData map(String line) {
        String[] fields = line.split(",");

        String symbol = fields[0];
        String date = fields[1];
        double open = Double.parseDouble(fields[2]);
        double high = Double.parseDouble(fields[2]);

        double low = Double.parseDouble(fields[4]);
        double close = Double.parseDouble(fields[5]);
        double adjClose = Double.parseDouble(fields[6]);
        long volume = Long.parseLong(fields[7]);
        QuoteData quoteData = new QuoteData(symbol, date, open, high, low, close, adjClose, volume);
        return quoteData;
    }



}
