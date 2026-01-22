package com.example.countdowntimer.viewmodel;

import android.app.Application;
import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import com.example.countdowntimer.database.EventEntity;
import com.example.countdowntimer.repository.EventRepository;
import java.util.List;

/**
 * 事件 ViewModel
 */
public class EventViewModel extends AndroidViewModel {
    
    private EventRepository repository;
    private LiveData<List<EventEntity>> allEvents;
    private LiveData<String> errorMessage;
    private LiveData<Boolean> isLoading;
    
    public EventViewModel(@NonNull Application application) {
        super(application);
        repository = new EventRepository(application);
        allEvents = repository.getAllEvents();
        errorMessage = repository.getErrorMessage();
        isLoading = repository.getIsLoading();
    }
    
    // ===== Getters =====
    
    public LiveData<List<EventEntity>> getAllEvents() {
        return allEvents;
    }
    
    public LiveData<List<EventEntity>> getEventsByStatus(String status) {
        return repository.getEventsByStatus(status);
    }
    
    public LiveData<List<EventEntity>> searchEvents(String query) {
        return repository.searchEvents(query);
    }
    
    public LiveData<EventEntity> getEvent(String name) {
        return repository.getEvent(name);
    }
    
    public LiveData<String> getErrorMessage() {
        return errorMessage;
    }
    
    public LiveData<Boolean> getIsLoading() {
        return isLoading;
    }
    
    // ===== 事件操作 =====
    
    public void createEvent(String name, String date) {
        repository.createEvent(name, date);
    }
    
    public void updateEvent(String name, String newDate) {
        repository.updateEvent(name, newDate);
    }
    
    public void deleteEvent(String name) {
        repository.deleteEvent(name);
    }
    
    public void syncAllEvents() {
        repository.syncAllEvents();
    }
}
