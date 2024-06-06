package com.kom.dsp.ClickAnalytics;

public class ClickLog {

    private String url;

    private String ip;

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public String getClientKey() {
        return clientKey;
    }

    public void setClientKey(String clientKey) {
        this.clientKey = clientKey;
    }

    private String clientKey;

    ClickLog(String url,  String ip, String clientKey){
        this.url = url;
        this.ip = ip;
        this.clientKey = clientKey;
    }


}
