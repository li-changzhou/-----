package com.example.countdowntimer.database;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;
import androidx.lifecycle.LiveData;
import java.util.List;

/**
 * 事件数据访问对象 (DAO)
 */
@Dao
public interface EventDao {
    
    /**
     * 获取所有事件
     */
    @Query("SELECT * FROM events ORDER BY daysRemaining ASC")
    LiveData<List<EventEntity>> getAllEvents();
    
    /**
     * 获取所有事件 (非 LiveData 版本)
     */
    @Query("SELECT * FROM events ORDER BY daysRemaining ASC")
    List<EventEntity> getAllEventsSync();
    
    /**
     * 按状态获取事件
     */
    @Query("SELECT * FROM events WHERE status = :status ORDER BY daysRemaining ASC")
    LiveData<List<EventEntity>> getEventsByStatus(String status);
    
    /**
     * 按名称获取事件
     */
    @Query("SELECT * FROM events WHERE name = :name")
    EventEntity getEventByName(String name);
    
    /**
     * 按名称获取事件 (LiveData)
     */
    @Query("SELECT * FROM events WHERE name = :name")
    LiveData<EventEntity> getEventByNameLive(String name);
    
    /**
     * 获取事件数量
     */
    @Query("SELECT COUNT(*) FROM events")
    int getEventCount();
    
    /**
     * 获取活跃事件数
     */
    @Query("SELECT COUNT(*) FROM events WHERE status = 'ACTIVE' OR status = 'CURRENT'")
    int getActiveEventCount();
    
    /**
     * 获取已过期事件数
     */
    @Query("SELECT COUNT(*) FROM events WHERE status = 'EXPIRED'")
    int getExpiredEventCount();
    
    /**
     * 获取下一个事件 (剩余天数最少的活跃事件)
     */
    @Query("SELECT * FROM events WHERE status = 'ACTIVE' OR status = 'CURRENT' " +
            "ORDER BY daysRemaining ASC LIMIT 1")
    EventEntity getNextEvent();
    
    /**
     * 插入事件
     */
    @Insert
    void insertEvent(EventEntity event);
    
    /**
     * 更新事件
     */
    @Update
    void updateEvent(EventEntity event);
    
    /**
     * 删除事件
     */
    @Delete
    void deleteEvent(EventEntity event);
    
    /**
     * 按名称删除事件
     */
    @Query("DELETE FROM events WHERE name = :name")
    void deleteEventByName(String name);
    
    /**
     * 删除所有事件
     */
    @Query("DELETE FROM events")
    void deleteAllEvents();
    
    /**
     * 搜索事件
     */
    @Query("SELECT * FROM events WHERE name LIKE '%' || :query || '%' " +
            "ORDER BY daysRemaining ASC")
    LiveData<List<EventEntity>> searchEvents(String query);
}
