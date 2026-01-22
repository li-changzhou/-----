package com.example.countdowntimer.api;

import com.example.countdowntimer.utils.Constants;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import okhttp3.OkHttpClient;
import java.util.concurrent.TimeUnit;

/**
 * API 客户端配置
 */
public class ApiClient {
    
    private static Retrofit retrofit;
    private static ApiService apiService;
    
    /**
     * 获取 Retrofit 实例
     */
    public static Retrofit getRetrofit() {
        if (retrofit == null) {
            OkHttpClient client = new OkHttpClient.Builder()
                    .connectTimeout(Constants.API_TIMEOUT, TimeUnit.SECONDS)
                    .readTimeout(Constants.API_TIMEOUT, TimeUnit.SECONDS)
                    .writeTimeout(Constants.API_TIMEOUT, TimeUnit.SECONDS)
                    .build();
            
            retrofit = new Retrofit.Builder()
                    .baseUrl(Constants.API_BASE_URL)
                    .client(client)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }
    
    /**
     * 获取 API 服务实例
     */
    public static ApiService getApiService() {
        if (apiService == null) {
            apiService = getRetrofit().create(ApiService.class);
        }
        return apiService;
    }
    
    /**
     * 重置客户端（用于切换 API 地址）
     */
    public static void reset() {
        retrofit = null;
        apiService = null;
    }
}
