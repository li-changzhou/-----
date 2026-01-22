package com.example.countdowntimer.database;

import android.content.Context;
import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;
import com.example.countdowntimer.utils.Constants;

/**
 * Room 数据库配置
 */
@Database(entities = {EventEntity.class}, version = Constants.DB_VERSION)
public abstract class EventDatabase extends RoomDatabase {
    
    public abstract EventDao eventDao();
    
    private static EventDatabase instance;
    
    /**
     * 获取数据库单例
     */
    public static synchronized EventDatabase getInstance(Context context) {
        if (instance == null) {
            instance = Room.databaseBuilder(
                    context.getApplicationContext(),
                    EventDatabase.class,
                    Constants.DB_NAME
            )
            .fallbackToDestructiveMigration()
            .build();
        }
        return instance;
    }
    
    /**
     * 销毁数据库实例（用于测试）
     */
    public static void destroyInstance() {
        instance = null;
    }
}
