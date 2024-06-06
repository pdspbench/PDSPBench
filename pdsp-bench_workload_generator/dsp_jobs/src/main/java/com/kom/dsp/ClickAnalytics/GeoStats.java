package com.kom.dsp.ClickAnalytics;

import java.util.HashMap;
import java.util.Map;

public class GeoStats {

    private String country;
    private Map<String, Integer> cityVisits;

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public Map<String, Integer> getCityVisits() {
        return cityVisits;
    }

    public void setCityVisits(Map<String, Integer> cityVisits) {
        this.cityVisits = cityVisits;
    }

    public GeoStats(String country) {
        this.country = country;
        this.cityVisits = new HashMap<>();
    }

    public void updateCityVisits(String city) {
        int visitCount = cityVisits.getOrDefault(city, 0);
        cityVisits.put(city, visitCount + 1);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("GeoStats{");
        sb.append("country='").append(country).append('\'');
        sb.append(", cityVisits={");
        for (Map.Entry<String, Integer> entry : cityVisits.entrySet()) {
            sb.append(entry.getKey()).append("=").append(entry.getValue()).append(", ");
        }
        if (!cityVisits.isEmpty()) {
            sb.setLength(sb.length() - 2); // Remove trailing comma and space
        }
        sb.append("}");
        sb.append('}');
        return sb.toString();
    }

}
