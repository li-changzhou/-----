package com.example.countdowntimer.fragments;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.countdowntimer.R;
import com.example.countdowntimer.adapters.EventAdapter;
import com.example.countdowntimer.viewmodel.EventViewModel;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

/**
 * 事件列表 Fragment
 */
public class EventListFragment extends Fragment {
    
    private EventViewModel viewModel;
    private RecyclerView recyclerView;
    private EventAdapter adapter;
    private EditText searchView;
    private FloatingActionButton fabAdd;
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                           @Nullable ViewGroup container,
                           @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_event_list, container, false);
    }
    
    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        
        // 初始化 ViewModel
        viewModel = new ViewModelProvider(this).get(EventViewModel.class);
        
        // 初始化 UI
        recyclerView = view.findViewById(R.id.recycler_view_events);
        searchView = view.findViewById(R.id.search_input);
        fabAdd = view.findViewById(R.id.fab_add_event);
        
        // 设置 RecyclerView
        adapter = new EventAdapter();
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);
        
        // 观察事件列表
        viewModel.getAllEvents().observe(getViewLifecycleOwner(), events -> {
            adapter.submitList(events);
        });
        
        // 搜索功能
        searchView.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                String query = s.toString().trim();
                if (query.isEmpty()) {
                    viewModel.getAllEvents().observe(getViewLifecycleOwner(), events -> {
                        adapter.submitList(events);
                    });
                } else {
                    viewModel.searchEvents(query).observe(getViewLifecycleOwner(), events -> {
                        adapter.submitList(events);
                    });
                }
            }
            
            @Override
            public void afterTextChanged(Editable s) {}
        });
        
        // 添加按钮
        fabAdd.setOnClickListener(v -> {
            // 跳转到添加事件 Fragment
            requireActivity().getSupportFragmentManager().beginTransaction()
                    .replace(R.id.nav_host_fragment, new AddEventFragment())
                    .addToBackStack(null)
                    .commit();
        });
    }
}
