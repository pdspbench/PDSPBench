package com.kom.dsp.ClickAnalytics;

import com.maxmind.geoip2.DatabaseReader;
import com.maxmind.geoip2.exception.AddressNotFoundException;
import com.maxmind.geoip2.exception.GeoIp2Exception;
import com.maxmind.geoip2.model.CityResponse;
import com.maxmind.geoip2.record.City;
import com.maxmind.geoip2.record.Country;
import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;

import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.net.URL;

import org.apache.flink.configuration.Configuration;

public class GeographyOperator extends ProcessFunction<ClickLog, GeoStats> {
    private transient DatabaseReader databaseReader;

    @Override
    public void open(Configuration parameters) throws Exception {
        
try {
    URL databaseURL = new URL("https://git.io/GeoLite2-City.mmdb");

    // Create the DatabaseReader.Builder using the URL
    databaseReader = new DatabaseReader.Builder(databaseURL.openStream()).build();
} catch (IOException e) {
    throw new RuntimeException("Failed to open GeoIP2 database", e);
}
    }

    @Override
    public void processElement(ClickLog event, Context ctx, Collector<GeoStats> out) throws Exception {
        // Perform IP lookup and extract city and country
        String ipAddress = event.getIp();
        try {
            String city = performCityLookup(ipAddress);
            String country = performCountryLookup(ipAddress);

            GeoStats geoStats = new GeoStats(country);
            geoStats.updateCityVisits(city);
            out.collect(geoStats);
        } catch(AddressNotFoundException e) {
            System.out.println("Address not found");
            GeoStats geoStats = new GeoStats("India");
            geoStats.updateCityVisits("Bangalore");
            out.collect(geoStats);
        }

    }

    private String performCityLookup(String ipAddress) throws IOException, GeoIp2Exception {
        InetAddress inetAddress = InetAddress.getByName(ipAddress);
        CityResponse response = databaseReader.city(inetAddress);
        City city = response.getCity();
        return city.getName();
    }

    private String performCountryLookup(String ipAddress) throws IOException, GeoIp2Exception {
        InetAddress inetAddress = InetAddress.getByName(ipAddress);
        CityResponse response = databaseReader.city(inetAddress);
        Country country = response.getCountry();
        return country.getName();
    }

    @Override
    public void close() throws IOException {
        // Close the database reader
        if (databaseReader != null) {
            databaseReader.close();
        }
    }
}
