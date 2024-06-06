package com.kom.dsp.TrafficMonitoring;



import java.io.*;

import java.net.URL;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import com.google.gson.Gson;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;




import org.slf4j.Logger;
import org.slf4j.LoggerFactory;



public class Helper {

    private static final Logger LOG = LoggerFactory.getLogger(Helper.class);


    public static Map<Long,Double[][]> roadMap = new HashMap<>();


    public static void loadShapeFile() throws IOException {

        DecimalFormat df = new DecimalFormat("#.##");
        LOG.info("Loading shape file");
        String geoJsonUrl =  "https://gitlab.com/sumalya/cloudlab_profile2/-/raw/master/roads.geojson?ref_type=heads&inline=false";
        //loading the file from flink bin
        URL url = new URL(geoJsonUrl);
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()))) {
            //googles Gson library
            Gson gson = new Gson();
            JsonObject jsonObject = gson.fromJson(reader, JsonObject.class);
            JsonArray featureArray = jsonObject.getAsJsonArray("features");
            for(int i = 0; i < featureArray.size(); i++){
                JsonObject featureObject = featureArray.get(i).getAsJsonObject();
                JsonObject props = featureObject.getAsJsonObject("properties");
                JsonArray coordinatesArray = featureObject.getAsJsonObject("geometry").getAsJsonArray("coordinates");
                Long osm_id = props.get("osm_id").getAsLong();
                Double[][] coordinates = new Double[coordinatesArray.size()][2];
                for (int j = 0; j < coordinatesArray.size(); j++) {
                    JsonArray coordinate = coordinatesArray.get(j).getAsJsonArray();
                    Double longitude = coordinate.get(0).getAsDouble();
                    Double latitude = coordinate.get(1).getAsDouble();
                    coordinates[j][0] = Double.parseDouble(df.format(longitude));
                    coordinates[j][1] = Double.parseDouble(df.format(latitude));
                }
                LOG.info("Osm_id:"+osm_id);
                roadMap.put(osm_id,coordinates);
            }
        } catch (Exception e){

        }

    }

}
