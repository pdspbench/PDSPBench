package com.kom.dsp.AdsAnalytics;

import java.io.Serializable;

public class RollingCTR implements Serializable {
    public long queryId;
    public long adId;
    public float clicks;
    public float impressions;
    public float ctrValue;

    public RollingCTR() {
    }

    public RollingCTR(long queryId, long adId, float clicks, float impressions, float ctrValue) {
        this.queryId = queryId;
        this.adId = adId;
        this.clicks = clicks;
        this.impressions = impressions;
        this.ctrValue = ctrValue;
    }

    public long getQueryId() {
        return queryId;
    }

    public void setQueryId(long queryId) {
        this.queryId = queryId;
    }

    public long getAdId() {
        return adId;
    }

    public void setAdId(long adId) {
        this.adId = adId;
    }

    public float getClicks() {
        return clicks;
    }

    public void setClicks(float clicks) {
        this.clicks = clicks;
    }

    public float getImpressions() {
        return impressions;
    }

    public void setImpressions(float impressions) {
        this.impressions = impressions;
    }

    public float getCtrValue() {
        return ctrValue;
    }

    public void setCtrValue(float ctrValue) {
        this.ctrValue = ctrValue;
    }

    @Override
    public String toString() {
        return "RollingCTR{" +
                "queryId=" + queryId +
                ", adId=" + adId +
                ", clicks=" + clicks +
                ", impressions=" + impressions +
                ", ctrValue=" + ctrValue +
                '}';
    }
}
