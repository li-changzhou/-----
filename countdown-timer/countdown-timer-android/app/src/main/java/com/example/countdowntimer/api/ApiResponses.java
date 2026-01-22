package com.example.countdowntimer.api;

import com.google.gson.annotations.SerializedName;
import java.util.List;

/**
 * API 事件列表响应
 */
public class EventListResponse {
    
    @SerializedName("events")
    public List<EventApiModel> events;
    
    @SerializedName("total")
    public int total;
    
    public EventListResponse() {
    }
}

/**
 * API 统计数据响应
 */
class StatsResponse {
    @SerializedName("total_events")
    public int totalEvents;
    
    @SerializedName("active_events")
    public int activeEvents;
    
    @SerializedName("expired_events")
    public int expiredEvents;
    
    @SerializedName("next_event")
    public String nextEvent;
    
    @SerializedName("next_event_days")
    public Integer nextEventDays;
}

/**
 * API 错误响应
 */
class ErrorResponse {
    @SerializedName("detail")
    public String detail;
    
    @SerializedName("code")
    public String code;
}
