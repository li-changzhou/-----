package com.example.countdowntimer.database;

import androidx.room.Entity;
import androidx.room.PrimaryKey;
import java.io.Serializable;

/**
 * 事件数据库实体
 */
@Entity(tableName = "events")
public class EventEntity implements Serializable {
    
    @PrimaryKey(autoGenerate = false)
    public String name;
    
    public String date;          // YYYY-MM-DD 格式
    public String status;        // ACTIVE, CURRENT, EXPIRED
    public int daysRemaining;
    public long createdAt;       // 创建时间戳
    public long syncedAt;        // 最后同步时间戳
    
    public EventEntity() {
    }
    
    public EventEntity(String name, String date) {
        this.name = name;
        this.date = date;
        this.status = "ACTIVE";
        this.daysRemaining = 0;
        this.createdAt = System.currentTimeMillis();
        this.syncedAt = System.currentTimeMillis();
    }
    
    @Override
    public String toString() {
        return "EventEntity{" +
                "name='" + name + '\'' +
                ", date='" + date + '\'' +
                ", status='" + status + '\'' +
                ", daysRemaining=" + daysRemaining +
                '}';
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        
        EventEntity event = (EventEntity) o;
        
        if (!name.equals(event.name)) return false;
        return date.equals(event.date);
    }
    
    @Override
    public int hashCode() {
        int result = name.hashCode();
        result = 31 * result + date.hashCode();
        return result;
    }
}
