package com.example.countdowntimer.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.lifecycle.LifecycleOwner;
import androidx.recyclerview.widget.DiffUtil;
import androidx.recyclerview.widget.ListAdapter;
import androidx.recyclerview.widget.RecyclerView;
import com.example.countdowntimer.R;
import com.example.countdowntimer.database.EventEntity;
import com.example.countdowntimer.viewmodel.EventViewModel;

/**
 * 事件列表适配器
 */
public class EventAdapter extends ListAdapter<EventEntity, EventAdapter.EventViewHolder> {
    
    private EventViewModel viewModel;
    private LifecycleOwner lifecycleOwner;
    
    public EventAdapter() {
        super(new DiffUtil.ItemCallback<EventEntity>() {
            @Override
            public boolean areItemsTheSame(@NonNull EventEntity oldItem, @NonNull EventEntity newItem) {
                return oldItem.name.equals(newItem.name);
            }
            
            @Override
            public boolean areContentsTheSame(@NonNull EventEntity oldItem, @NonNull EventEntity newItem) {
                return oldItem.equals(newItem);
            }
        });
    }
    
    @NonNull
    @Override
    public EventViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_event, parent, false);
        return new EventViewHolder(view);
    }
    
    @Override
    public void onBindViewHolder(@NonNull EventViewHolder holder, int position) {
        EventEntity event = getItem(position);
        holder.bind(event);
    }
    
    public void setViewModel(EventViewModel viewModel, LifecycleOwner lifecycleOwner) {
        this.viewModel = viewModel;
        this.lifecycleOwner = lifecycleOwner;
    }
    
    /**
     * 事件卡片 ViewHolder
     */
    static class EventViewHolder extends RecyclerView.ViewHolder {
        
        private TextView nameView;
        private TextView dateView;
        private TextView daysView;
        private TextView statusView;
        private Button editButton;
        private Button deleteButton;
        
        public EventViewHolder(@NonNull View itemView) {
            super(itemView);
            nameView = itemView.findViewById(R.id.text_event_name);
            dateView = itemView.findViewById(R.id.text_event_date);
            daysView = itemView.findViewById(R.id.text_days_remaining);
            statusView = itemView.findViewById(R.id.text_event_status);
            editButton = itemView.findViewById(R.id.btn_edit);
            deleteButton = itemView.findViewById(R.id.btn_delete);
        }
        
        public void bind(EventEntity event) {
            nameView.setText(event.name);
            dateView.setText("📅 " + event.date);
            daysView.setText(String.valueOf(event.daysRemaining) + " 天");
            
            // 设置状态显示
            String statusText = "";
            int statusColor = 0;
            switch (event.status) {
                case "ACTIVE":
                    statusText = "进行中";
                    statusColor = itemView.getContext().getColor(R.color.status_active);
                    break;
                case "CURRENT":
                    statusText = "即将";
                    statusColor = itemView.getContext().getColor(R.color.status_current);
                    break;
                case "EXPIRED":
                    statusText = "已过期";
                    statusColor = itemView.getContext().getColor(R.color.status_expired);
                    break;
            }
            statusView.setText(statusText);
            statusView.setTextColor(statusColor);
            
            // 删除按钮
            deleteButton.setOnClickListener(v -> {
                // TODO: 实现删除逻辑
            });
        }
    }
}
