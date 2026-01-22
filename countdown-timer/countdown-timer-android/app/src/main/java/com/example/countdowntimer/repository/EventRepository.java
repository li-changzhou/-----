package com.example.countdowntimer.repository;

import android.content.Context;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import com.example.countdowntimer.api.ApiClient;
import com.example.countdowntimer.api.ApiService;
import com.example.countdowntimer.api.EventApiModel;
import com.example.countdowntimer.api.EventListResponse;
import com.example.countdowntimer.database.EventDatabase;
import com.example.countdowntimer.database.EventEntity;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import java.util.List;

/**
 * 事件数据仓库 (本地 + 网络)
 */
public class EventRepository {
    
    private EventDatabase database;
    private ApiService apiService;
    private MutableLiveData<String> errorMessage = new MutableLiveData<>();
    private MutableLiveData<Boolean> isLoading = new MutableLiveData<>();
    
    public EventRepository(Context context) {
        this.database = EventDatabase.getInstance(context);
        this.apiService = ApiClient.getApiService();
    }
    
    // ===== 观察者 =====
    
    public LiveData<List<EventEntity>> getAllEvents() {
        return database.eventDao().getAllEvents();
    }
    
    public LiveData<List<EventEntity>> getEventsByStatus(String status) {
        return database.eventDao().getEventsByStatus(status);
    }
    
    public LiveData<List<EventEntity>> searchEvents(String query) {
        return database.eventDao().searchEvents(query);
    }
    
    public LiveData<String> getErrorMessage() {
        return errorMessage;
    }
    
    public LiveData<Boolean> getIsLoading() {
        return isLoading;
    }
    
    // ===== 事件操作 =====
    
    /**
     * 创建事件 (先本地，后网络)
     */
    public void createEvent(String name, String date) {
        isLoading.setValue(true);
        
        // 1. 保存到本地
        EventEntity entity = new EventEntity(name, date);
        database.eventDao().insertEvent(entity);
        
        // 2. 同步到服务器
        EventApiModel apiModel = new EventApiModel(name, date);
        apiService.createEvent(apiModel).enqueue(new Callback<EventApiModel>() {
            @Override
            public void onResponse(Call<EventApiModel> call, Response<EventApiModel> response) {
                isLoading.setValue(false);
                if (response.isSuccessful() && response.body() != null) {
                    // 更新本地数据
                    EventEntity updated = new EventEntity(
                            response.body().name,
                            response.body().date
                    );
                    updated.status = response.body().status;
                    updated.daysRemaining = response.body().daysRemaining;
                    updated.syncedAt = System.currentTimeMillis();
                    database.eventDao().updateEvent(updated);
                } else {
                    errorMessage.setValue("创建事件失败");
                }
            }
            
            @Override
            public void onFailure(Call<EventApiModel> call, Throwable t) {
                isLoading.setValue(false);
                errorMessage.setValue("网络错误: " + t.getMessage());
            }
        });
    }
    
    /**
     * 获取事件详情
     */
    public LiveData<EventEntity> getEvent(String name) {
        return database.eventDao().getEventByNameLive(name);
    }
    
    /**
     * 更新事件
     */
    public void updateEvent(String name, String newDate) {
        isLoading.setValue(true);
        
        // 1. 获取当前事件
        EventEntity current = database.eventDao().getEventByName(name);
        if (current != null) {
            current.date = newDate;
            current.syncedAt = System.currentTimeMillis();
            database.eventDao().updateEvent(current);
        }
        
        // 2. 同步到服务器
        EventApiModel apiModel = new EventApiModel(name, newDate);
        apiService.updateEvent(name, apiModel).enqueue(new Callback<EventApiModel>() {
            @Override
            public void onResponse(Call<EventApiModel> call, Response<EventApiModel> response) {
                isLoading.setValue(false);
                if (response.isSuccessful() && response.body() != null) {
                    EventEntity updated = new EventEntity(
                            response.body().name,
                            response.body().date
                    );
                    updated.status = response.body().status;
                    updated.daysRemaining = response.body().daysRemaining;
                    updated.syncedAt = System.currentTimeMillis();
                    database.eventDao().updateEvent(updated);
                } else {
                    errorMessage.setValue("更新事件失败");
                }
            }
            
            @Override
            public void onFailure(Call<EventApiModel> call, Throwable t) {
                isLoading.setValue(false);
                errorMessage.setValue("网络错误: " + t.getMessage());
            }
        });
    }
    
    /**
     * 删除事件
     */
    public void deleteEvent(String name) {
        isLoading.setValue(true);
        
        // 1. 从本地删除
        database.eventDao().deleteEventByName(name);
        
        // 2. 从服务器删除
        apiService.deleteEvent(name).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                isLoading.setValue(false);
                if (!response.isSuccessful()) {
                    errorMessage.setValue("删除事件失败");
                }
            }
            
            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                isLoading.setValue(false);
                errorMessage.setValue("网络错误: " + t.getMessage());
            }
        });
    }
    
    /**
     * 同步所有事件 (从服务器获取最新数据)
     */
    public void syncAllEvents() {
        isLoading.setValue(true);
        
        apiService.listEvents(null).enqueue(new Callback<EventListResponse>() {
            @Override
            public void onResponse(Call<EventListResponse> call, Response<EventListResponse> response) {
                isLoading.setValue(false);
                if (response.isSuccessful() && response.body() != null) {
                    // 清空本地数据
                    database.eventDao().deleteAllEvents();
                    
                    // 插入新数据
                    for (EventApiModel apiEvent : response.body().events) {
                        EventEntity entity = new EventEntity(apiEvent.name, apiEvent.date);
                        entity.status = apiEvent.status;
                        entity.daysRemaining = apiEvent.daysRemaining;
                        entity.syncedAt = System.currentTimeMillis();
                        database.eventDao().insertEvent(entity);
                    }
                } else {
                    errorMessage.setValue("同步失败");
                }
            }
            
            @Override
            public void onFailure(Call<EventListResponse> call, Throwable t) {
                isLoading.setValue(false);
                errorMessage.setValue("网络错误: " + t.getMessage());
            }
        });
    }
}
