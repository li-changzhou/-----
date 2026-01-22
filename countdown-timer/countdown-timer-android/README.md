# 🚀 Event Countdown Android 应用 - 快速启动指南

**应用名称**: Event Countdown  
**版本**: 1.0.0  
**语言**: Java  
**API 等级**: 26-34  
**状态**: ✅ 开发完成

---

## 📱 应用功能

### 核心功能
- ✅ **事件管理** - 创建、编辑、删除事件
- ✅ **实时倒计时** - 显示事件距今天数
- ✅ **本地存储** - Room 数据库持久化
- ✅ **服务器同步** - 与 Python 后端同步
- ✅ **搜索功能** - 快速查找事件
- ✅ **统计信息** - 事件统计面板

### UI 特性
- 🎨 Material Design 3
- 📱 响应式布局
- 🌙 深色模式支持（计划中）
- ♿ 无障碍支持

---

## 🛠️ 环境要求

### 必需工具
- **Android Studio** 2023.1 或更新版本
- **Java JDK** 17 或更新版本
- **Android SDK** 34 或更新版本
- **Android Emulator** 或真机设备

### 推荐配置
- **IDE**: Android Studio Giraffe (2023.1.1)
- **Gradle**: 8.0+
- **Min SDK**: 26 (Android 8.0)
- **Target SDK**: 34 (Android 14)

---

## 🚀 快速启动

### 1️⃣ 打开项目

```bash
# 使用 Android Studio 打开项目
File → Open → countdown-timer-android/
```

### 2️⃣ 配置后端 API

编辑 `Constants.java`，设置 API 地址：

```java
// src/main/java/com/example/countdowntimer/utils/Constants.java

public static final String API_BASE_URL = "http://10.0.2.2:8000/"; // 模拟器
// 或
public static final String API_BASE_URL = "http://192.168.1.x:8000/"; // 真机
```

**说明**:
- `10.0.2.2` - Android 模拟器访问本机的特殊 IP
- `192.168.1.x` - 替换为你的电脑在局域网中的 IP 地址

### 3️⃣ 构建项目

```bash
# 或在 Android Studio 中：Build → Make Project
./gradlew build
```

### 4️⃣ 运行应用

#### 方式 A: 使用模拟器
```bash
# 创建虚拟设备（如果还没有）
Android Studio → Virtual Device Manager → Create Device

# 或使用 Android Studio 的 Run 按钮
```

#### 方式 B: 使用真机
```bash
# 1. 连接 Android 手机
# 2. 启用开发者选项和 USB 调试
# 3. 在 Android Studio 中选择设备并点击 Run
```

### 5️⃣ 安装 APK

```bash
# 从命令行安装
./gradlew installDebug

# 或打开生成的 APK
build/outputs/apk/debug/app-debug.apk
```

---

## 📂 项目结构说明

```
countdown-timer-android/
├── app/src/main/
│   ├── java/com/example/countdowntimer/
│   │   ├── activities/          # Activity 类
│   │   │   └── MainActivity.java
│   │   │
│   │   ├── fragments/           # Fragment 类
│   │   │   ├── EventListFragment.java
│   │   │   └── AddEventFragment.java
│   │   │
│   │   ├── adapters/            # RecyclerView 适配器
│   │   │   └── EventAdapter.java
│   │   │
│   │   ├── api/                 # API 相关
│   │   │   ├── ApiService.java
│   │   │   ├── ApiClient.java
│   │   │   └── EventApiModel.java
│   │   │
│   │   ├── database/            # Room 数据库
│   │   │   ├── EventDatabase.java
│   │   │   ├── EventDao.java
│   │   │   └── EventEntity.java
│   │   │
│   │   ├── repository/          # 数据仓库层
│   │   │   └── EventRepository.java
│   │   │
│   │   ├── viewmodel/           # ViewModel
│   │   │   └── EventViewModel.java
│   │   │
│   │   └── utils/               # 工具类
│   │       └── Constants.java
│   │
│   └── res/
│       ├── layout/              # XML 布局
│       ├── values/              # 资源文件
│       ├── drawable/            # 图标资源
│       └── menu/                # 菜单定义
│
├── build.gradle                 # 项目级 Gradle
├── settings.gradle              # 项目设置
└── README.md                    # 项目说明
```

---

## 🔄 应用工作流

### 数据流向

```
User Interface (Activity/Fragment)
        ↓
ViewModel (状态管理)
        ↓
Repository (数据源抽象)
        ↓↘
   ↙    ↓    ↖
Local DB  API  (Retrofit)
```

### 事件创建流程

```
1. 用户在 AddEventFragment 输入信息
       ↓
2. 点击保存按钮
       ↓
3. ViewModel.createEvent() 调用
       ↓
4. Repository 保存到本地数据库
       ↓
5. Repository 发送到服务器
       ↓
6. 服务器响应后更新本地记录
       ↓
7. UI 自动刷新 (LiveData)
```

---

## 🧪 测试应用

### 单元测试

```bash
# 运行所有单元测试
./gradlew test

# 运行特定测试
./gradlew test --tests com.example.countdowntimer.utils.*
```

### 集成测试 (Instrumented Tests)

```bash
# 运行设备上的测试
./gradlew connectedAndroidTest

# 需要连接模拟器或真机
```

### 手动测试场景

- ✅ 创建事件 - 输入名称和日期，验证显示
- ✅ 编辑事件 - 修改事件日期
- ✅ 删除事件 - 确认删除操作
- ✅ 搜索事件 - 输入关键字筛选
- ✅ 离线使用 - 关闭网络，验证本地数据可用
- ✅ 服务器同步 - 连接网络后同步数据

---

## 🔧 常见问题排查

### 问题 1: 编译错误 - Gradle 版本不匹配

**症状**: `Could not find com.android.tools.build:gradle`

**解决方案**:
```bash
# 更新 Gradle 包装器
./gradlew wrapper --gradle-version 8.0

# 或在 Android Studio 中：File → Project Structure → Project
```

### 问题 2: API 连接失败

**症状**: `Failed to connect to 10.0.2.2:8000`

**排查步骤**:
1. 确认 FastAPI 后端正在运行
   ```bash
   python app.py
   ```

2. 在模拟器中测试连接
   ```bash
   adb shell
   curl http://10.0.2.2:8000/health
   ```

3. 查看 Logcat 日志
   ```bash
   adb logcat | grep -i countdown
   ```

### 问题 3: 数据库错误

**症状**: `AndroidRuntime: java.lang.RuntimeException: unable to start activity...`

**解决方案**:
```bash
# 清除应用数据
adb shell pm clear com.example.countdowntimer

# 重新安装应用
./gradlew installDebug
```

### 问题 4: 权限问题

**症状**: `Permission denied (13)`

**解决方案**:
- 检查 AndroidManifest.xml 中的权限声明
- 对于 Android 6+，在运行时请求权限
- 在真机上手动授予权限

---

## 📊 项目统计

| 指标 | 值 |
|------|-----|
| Java 源文件 | 12 个 |
| XML 布局文件 | 5 个 |
| 资源文件 | 8 个 |
| 总代码行数 | 1500+ 行 |
| 最低 API | 26 (Android 8.0) |
| 目标 API | 34 (Android 14) |

---

## 🎯 下一步功能

### 短期 (v1.1)
- [ ] 深色模式
- [ ] 推送通知
- [ ] 本地化 (多语言)

### 中期 (v1.2)
- [ ] 事件重复设置
- [ ] 日历视图
- [ ] 导出功能

### 长期 (v2.0)
- [ ] 离线优先架构
- [ ] 云同步
- [ ] 团队协作

---

## 📝 开发日志

### 版本 1.0.0 (当前)
- ✅ 核心功能实现
- ✅ Material Design UI
- ✅ 本地数据库
- ✅ API 集成
- ✅ 错误处理

---

## 📞 支持和反馈

如遇到问题，请：

1. 查看 Logcat 日志
2. 检查 API 连接
3. 检查数据库状态
4. 查阅本文档

---

## 📄 许可证

[项目许可证 - 待定]

---

**App Countdown - 让你不再错过重要日期！** 🎯

**状态**: ✅ 生产就绪  
**最后更新**: 2026-01-22
