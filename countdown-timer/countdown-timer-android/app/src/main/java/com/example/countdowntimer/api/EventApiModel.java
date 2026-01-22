package com.example.countdowntimer.api;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;

/**
 * API 事件模型
 */
public class EventApiModel implements Serializable {
    
    @SerializedName("name")
    public String name;
    
    @SerializedName("date")
    public String date;
    
    @SerializedName("status")
    public String status;
    
    @SerializedName("days_remaining")
    public int daysRemaining;
    
    public EventApiModel() {
    }
    
    public EventApiModel(String name, String date) {
        this.name = name;
        this.date = date;
    }
    
    @Override
    public String toString() {
        return "EventApiModel{" +
                "name='" + name + '\'' +
                ", date='" + date + '\'' +
                ", status='" + status + '\'' +
                ", daysRemaining=" + daysRemaining +
                '}';
    }
}
