package com.example.countdowntimer.fragments;

import android.app.DatePickerDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.DatePicker;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import com.example.countdowntimer.R;
import com.example.countdowntimer.viewmodel.EventViewModel;
import com.google.android.material.snackbar.Snackbar;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Locale;

/**
 * 添加事件 Fragment
 */
public class AddEventFragment extends Fragment implements DatePickerDialog.OnDateSetListener {
    
    private EventViewModel viewModel;
    private EditText nameInput;
    private EditText dateInput;
    private Button saveButton;
    private Button cancelButton;
    private Calendar selectedDate;
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                           @Nullable ViewGroup container,
                           @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_add_event, container, false);
    }
    
    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        
        // 初始化 ViewModel
        viewModel = new ViewModelProvider(this).get(EventViewModel.class);
        
        // 初始化 UI
        nameInput = view.findViewById(R.id.input_event_name);
        dateInput = view.findViewById(R.id.input_event_date);
        saveButton = view.findViewById(R.id.btn_save);
        cancelButton = view.findViewById(R.id.btn_cancel);
        
        // 初始化日期
        selectedDate = Calendar.getInstance();
        selectedDate.add(Calendar.DAY_OF_MONTH, 1); // 默认明天
        updateDateDisplay();
        
        // 日期选择
        dateInput.setOnClickListener(v -> showDatePicker());
        
        // 保存按钮
        saveButton.setOnClickListener(v -> saveEvent());
        
        // 取消按钮
        cancelButton.setOnClickListener(v -> requireActivity().onBackPressed());
        
        // 监听错误信息
        viewModel.getErrorMessage().observe(getViewLifecycleOwner(), error -> {
            if (error != null && !error.isEmpty()) {
                Snackbar.make(view, error, Snackbar.LENGTH_SHORT).show();
            }
        });
    }
    
    private void showDatePicker() {
        DatePickerDialog dialog = new DatePickerDialog(
                requireContext(),
                this,
                selectedDate.get(Calendar.YEAR),
                selectedDate.get(Calendar.MONTH),
                selectedDate.get(Calendar.DAY_OF_MONTH)
        );
        dialog.show();
    }
    
    @Override
    public void onDateSet(DatePicker view, int year, int month, int dayOfMonth) {
        selectedDate.set(year, month, dayOfMonth);
        updateDateDisplay();
    }
    
    private void updateDateDisplay() {
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
        dateInput.setText(format.format(selectedDate.getTime()));
    }
    
    private void saveEvent() {
        String name = nameInput.getText().toString().trim();
        String date = dateInput.getText().toString().trim();
        
        if (name.isEmpty()) {
            Snackbar.make(requireView(), "请输入事件名称", Snackbar.LENGTH_SHORT).show();
            return;
        }
        
        if (date.isEmpty()) {
            Snackbar.make(requireView(), "请选择事件日期", Snackbar.LENGTH_SHORT).show();
            return;
        }
        
        // 创建事件
        viewModel.createEvent(name, date);
        
        // 返回列表
        requireActivity().onBackPressed();
    }
}
