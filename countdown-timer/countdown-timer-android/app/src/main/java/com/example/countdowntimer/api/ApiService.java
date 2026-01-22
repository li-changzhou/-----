package com.example.countdowntimer.api;

import retrofit2.Call;
import retrofit2.http.*;
import java.util.List;

/**
 * Retrofit API 服务接口
 */
public interface ApiService {
    
    // ===== 事件操作 =====
    
    @GET("api/events")
    Call<EventListResponse> listEvents(
            @Query("status") String status
    );
    
    @POST("api/events")
    Call<EventApiModel> createEvent(
            @Body EventApiModel event
    );
    
    @GET("api/events/{name}")
    Call<EventApiModel> getEvent(
            @Path("name") String name
    );
    
    @PUT("api/events/{name}")
    Call<EventApiModel> updateEvent(
            @Path("name") String name,
            @Body EventApiModel event
    );
    
    @DELETE("api/events/{name}")
    Call<Void> deleteEvent(
            @Path("name") String name
    );
    
    // ===== 统计数据 =====
    
    @GET("api/stats")
    Call<StatsResponse> getStats();
    
    // ===== 健康检查 =====
    
    @GET("health")
    Call<HealthResponse> healthCheck();
}

/**
 * 健康检查响应
 */
class HealthResponse {
    public String status;
    public String version;
}
