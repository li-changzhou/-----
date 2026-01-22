package com.example.countdowntimer.utils;

/**
 * 应用常量定义
 */
public class Constants {
    
    // API 配置
    public static final String API_BASE_URL = "http://10.0.2.2:8000/";
    // public static final String API_BASE_URL = "http://192.168.1.x:8000/"; // 替换为你的服务器 IP
    public static final int API_TIMEOUT = 30; // 秒
    ·
    // 数据库
    public static final String DB_NAME = "countdown_db";
    public static final int DB_VERSION = 1;
    
    // SharedPreferences
    public static final String PREF_NAME = "countdown_prefs";
    public static final String PREF_SYNC_TIME = "last_sync_time";
    public static final String PREF_AUTO_SYNC = "auto_sync";
    public static final String PREF_NOTIFICATION_ENABLED = "notification_enabled";
    
    // 通知
    public static final String NOTIFICATION_CHANNEL_ID = "countdown_events";
    public static final String NOTIFICATION_CHANNEL_NAME = "倒计时事件";
    public static final int NOTIFICATION_ID_BASE = 1000;
    
    // 日期格式
    public static final String DATE_FORMAT_DISPLAY = "yyyy年M月d日 EEEE";
    public static final String DATE_FORMAT_ISO = "yyyy-MM-dd";
    
    // 事件状态
    public static final String EVENT_STATUS_ACTIVE = "ACTIVE";
    public static final String EVENT_STATUS_CURRENT = "CURRENT";
    public static final String EVENT_STATUS_EXPIRED = "EXPIRED";
    
    // 请求代码
    public static final int REQ_CODE_ADD_EVENT = 100;
    public static final int REQ_CODE_EDIT_EVENT = 101;
    
    // 刷新间隔 (毫秒)
    public static final long REFRESH_INTERVAL = 60000; // 1 分钟
}
