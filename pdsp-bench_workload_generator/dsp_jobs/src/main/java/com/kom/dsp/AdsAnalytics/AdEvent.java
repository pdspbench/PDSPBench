package com.kom.dsp.AdsAnalytics;

import java.io.Serializable;

public class AdEvent implements Serializable {
    public String type;
    public int clicks;
    public int views;
    public String display_url;
    public long adId;
    public long advertiserId;
    public int depth;
    public long position;
    public long queryId;
    public long keywordId;
    public long titleId;
    public long descriptionId;
    public long userId;
    public float count;

    public AdEvent() {
    }

    public AdEvent(String type, int clicks, int views, String display_url, long adId, long advertiserId, int depth, int position, long queryId, long keywordId, long titleId, long descriptionId, long userId, float count) {
        this.type = type;
        this.clicks = clicks;
        this.views = views;
        this.display_url = display_url;
        this.adId = adId;
        this.advertiserId = advertiserId;
        this.depth = depth;
        this.position = position;
        this.queryId = queryId;
        this.keywordId = keywordId;
        this.titleId = titleId;
        this.descriptionId = descriptionId;
        this.userId = userId;
        this.count = count;
    }


    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getClicks() {
        return clicks;
    }

    public void setClicks(int clicks) {
        this.clicks = clicks;
    }

    public int getViews() {
        return views;
    }

    public void setViews(int views) {
        this.views = views;
    }

    public String getDisplay_url() {
        return display_url;
    }

    public void setDisplay_url(String display_url) {
        this.display_url = display_url;
    }

    public long getAdId() {
        return adId;
    }

    public void setAdId(long adId) {
        this.adId = adId;
    }

    public long getAdvertiserId() {
        return advertiserId;
    }

    public void setAdvertiserId(long advertiserId) {
        this.advertiserId = advertiserId;
    }

    public int getDepth() {
        return depth;
    }

    public void setDepth(int depth) {
        this.depth = depth;
    }

    public long getPosition() {
        return position;
    }

    public void setPosition(long position) {
        this.position = position;
    }

    public long getQueryId() {
        return queryId;
    }

    public void setQueryId(long queryId) {
        this.queryId = queryId;
    }

    public long getKeywordId() {
        return keywordId;
    }

    public void setKeywordId(long keywordId) {
        this.keywordId = keywordId;
    }

    public long getTitleId() {
        return titleId;
    }

    public void setTitleId(long titleId) {
        this.titleId = titleId;
    }

    public long getDescriptionId() {
        return descriptionId;
    }

    public void setDescriptionId(long descriptionId) {
        this.descriptionId = descriptionId;
    }

    public long getUserId() {
        return userId;
    }

    public void setUserId(long userId) {
        this.userId = userId;
    }

    public float getCount() {
        return count;
    }

    public void setCount(float count) {
        this.count = count;
    }

    @Override
    public String toString() {
        return "AdEvent{" +
                "type='" + type + '\'' +
                ", clicks=" + clicks +
                ", views=" + views +
                ", display_url='" + display_url + '\'' +
                ", adId=" + adId +
                ", advertiserId=" + advertiserId +
                ", depth=" + depth +
                ", position=" + position +
                ", queryId=" + queryId +
                ", keywordId=" + keywordId +
                ", titleId=" + titleId +
                ", descriptionId=" + descriptionId +
                ", userId=" + userId +
                ", count=" + count +
                '}';
    }
}
