package com.example.countdowntimer.activities;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.navigation.NavController;
import androidx.navigation.fragment.NavHostFragment;
import androidx.navigation.ui.NavigationUI;
import com.example.countdowntimer.R;
import com.google.android.material.bottomnavigation.BottomNavigationView;

/**
 * 主 Activity - 应用入口
 */
public class MainActivity extends AppCompatActivity {
    
    private BottomNavigationView bottomNavigation;
    private NavController navController;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // 获取 NavHostFragment
        NavHostFragment navHostFragment = (NavHostFragment) getSupportFragmentManager()
                .findFragmentById(R.id.nav_host_fragment);
        
        if (navHostFragment != null) {
            navController = navHostFragment.getNavController();
            
            // 设置底部导航
            bottomNavigation = findViewById(R.id.bottom_navigation);
            NavigationUI.setupWithNavController(bottomNavigation, navController);
        }
    }
    
    @Override
    public boolean onSupportNavigateUp() {
        return navController.navigateUp() || super.onSupportNavigateUp();
    }
}
