package com.kom.dsp.LogsAnalyzer;

import org.apache.flink.api.common.functions.MapFunction;

// Function to parse the log data into LogEvent objects
public class LogParser implements MapFunction<String, LogEvent> {

    @Override
    public LogEvent map(String value) throws Exception {
        // Parse the log data and create a LogEvent object
        // You may need to customize this logic based on the log format
        // Example: "54.36.149.41 - - [22/Jan/2019:03:56:14 +0330] "GET /filter/27|13%20%D9%85%DA%AF%D8%A7%D9%BE%DB%8C%DA%A9%D8%B3%D9%84,27|%DA%A9%D9%85%D8%AA%D8%B1%20%D8%A7%D8%B2%205%20%D9%85%DA%AF%D8%A7%D9%BE%DB%8C%DA%A9%D8%B3%D9%84,p53 HTTP/1.1" 200 30577 "-" "Mozilla/5.0 (compatible; AhrefsBot/6.1; +http://ahrefs.com/robot/)" "-"

        System.out.println("this is printed:"+value);
        String[] parts = value.split(" ");
        for(String part : parts){
            System.out.println(part);
        }
        String logTime = parts[3].substring(1);
        String statusCode = value.split("\"")[2].trim().split(" ")[0];
        System.out.println(statusCode);
        return new LogEvent(logTime, statusCode);
    }
}