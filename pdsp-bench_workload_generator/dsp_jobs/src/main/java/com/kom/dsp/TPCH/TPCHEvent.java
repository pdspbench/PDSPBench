package com.kom.dsp.TPCH;

public class TPCHEvent {
    private String orderKey;

    private String cname;

    private String caddress;
    private int orderPriority;
    private double extendedPrice;
    private double discount;

    public TPCHEvent(String orderKey, String cname, String caddress, int orderPriority, double extendedPrice, double discount) {
        this.orderKey = orderKey;
        this.cname = cname;
        this.caddress = caddress;
        this.orderPriority = orderPriority;
        this.extendedPrice = extendedPrice;
        this.discount = discount;
    }

    public TPCHEvent() {

    }

    public String getOrderKey() {
        return orderKey;
    }

    public void setOrderKey(String orderKey) {
        this.orderKey = orderKey;
    }

    public String getCname() {
        return cname;
    }

    public void setCname(String cname) {
        this.cname = cname;
    }

    public String getCaddress() {
        return caddress;
    }

    public void setCaddress(String caddress) {
        this.caddress = caddress;
    }

    public int getOrderPriority() {
        return orderPriority;
    }

    public void setOrderPriority(int orderPriority) {
        this.orderPriority = orderPriority;
    }

    public double getExtendedPrice() {
        return extendedPrice;
    }

    public void setExtendedPrice(double extendedPrice) {
        this.extendedPrice = extendedPrice;
    }

    public double getDiscount() {
        return discount;
    }

    public void setDiscount(double discount) {
        this.discount = discount;
    }

    /*public int compareTo(String s) {
        return this.orderPriority.compareTo(s);
    }*/
}