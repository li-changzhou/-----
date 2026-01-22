"""API 集成测试"""

import pytest
from fastapi.testclient import TestClient
from src.countdown_timer.api.app import app
from datetime import date, timedelta
import json


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def cleanup():
    """在每个测试前后清理数据"""
    # 清理之前的数据
    from src.countdown_timer.storage import EventStorage
    storage = EventStorage()
    storage.clear_all()
    
    yield
    
    # 测试后清理
    storage.clear_all()


class TestHealth:
    """健康检查测试"""
    
    def test_health_check(self, client):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.2.0"


class TestEventCRUD:
    """事件 CRUD 操作测试"""
    
    def test_create_event(self, client):
        """测试创建事件"""
        tomorrow = date.today() + timedelta(days=1)
        response = client.post(
            "/api/events",
            json={
                "name": "生日",
                "date": tomorrow.isoformat()
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "生日"
        assert data["status"] == "ACTIVE"
    
    def test_get_event(self, client):
        """测试获取单个事件"""
        tomorrow = date.today() + timedelta(days=1)
        
        # 先创建事件
        client.post(
            "/api/events",
            json={"name": "测试", "date": tomorrow.isoformat()}
        )
        
        # 获取事件
        response = client.get("/api/events/测试")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "测试"
    
    def test_list_events(self, client):
        """测试列出所有事件"""
        tomorrow = date.today() + timedelta(days=1)
        
        # 创建多个事件
        for i in range(3):
            client.post(
                "/api/events",
                json={"name": f"事件{i}", "date": tomorrow.isoformat()}
            )
        
        # 获取列表
        response = client.get("/api/events")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["events"]) == 3
    
    def test_update_event(self, client):
        """测试更新事件"""
        tomorrow = date.today() + timedelta(days=1)
        next_week = date.today() + timedelta(days=7)
        
        # 创建事件
        client.post(
            "/api/events",
            json={"name": "会议", "date": tomorrow.isoformat()}
        )
        
        # 更新事件
        response = client.put(
            "/api/events/会议",
            json={"date": next_week.isoformat()}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == next_week.isoformat()
    
    def test_delete_event(self, client):
        """测试删除事件"""
        tomorrow = date.today() + timedelta(days=1)
        
        # 创建事件
        client.post(
            "/api/events",
            json={"name": "删除测试", "date": tomorrow.isoformat()}
        )
        
        # 删除事件
        response = client.delete("/api/events/删除测试")
        assert response.status_code == 204
        
        # 验证已删除
        response = client.get("/api/events/删除测试")
        assert response.status_code == 404


class TestEventStatus:
    """事件状态测试"""
    
    def test_active_event(self, client):
        """测试 ACTIVE 状态"""
        tomorrow = date.today() + timedelta(days=1)
        
        response = client.post(
            "/api/events",
            json={"name": "活跃事件", "date": tomorrow.isoformat()}
        )
        
        data = response.json()
        assert data["status"] == "ACTIVE"
        assert data["days_remaining"] == 1
    
    def test_expired_event(self, client):
        """测试 EXPIRED 状态"""
        yesterday = date.today() - timedelta(days=1)
        
        response = client.post(
            "/api/events",
            json={"name": "已过期", "date": yesterday.isoformat()}
        )
        
        data = response.json()
        assert data["status"] == "EXPIRED"
        assert data["days_remaining"] == 0
    
    def test_current_event(self, client):
        """测试 CURRENT 状态"""
        today = date.today()
        
        response = client.post(
            "/api/events",
            json={"name": "今天", "date": today.isoformat()}
        )
        
        data = response.json()
        assert data["status"] == "CURRENT"
        assert data["days_remaining"] == 0


class TestStats:
    """统计数据测试"""
    
    def test_get_stats(self, client):
        """测试获取统计数据"""
        tomorrow = date.today() + timedelta(days=1)
        yesterday = date.today() - timedelta(days=1)
        
        # 创建不同状态的事件
        client.post("/api/events", json={"name": "未来", "date": tomorrow.isoformat()})
        client.post("/api/events", json={"name": "过去", "date": yesterday.isoformat()})
        
        response = client.get("/api/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_events"] == 2
        assert data["active_events"] == 1
        assert data["expired_events"] == 1
        assert data["next_event"] == "未来"


class TestErrorHandling:
    """错误处理测试"""
    
    def test_invalid_date_format(self, client):
        """测试无效日期格式"""
        response = client.post(
            "/api/events",
            json={"name": "测试", "date": "invalid-date"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client):
        """测试缺少必需字段"""
        response = client.post("/api/events", json={"name": "测试"})
        assert response.status_code == 422
    
    def test_get_nonexistent_event(self, client):
        """测试获取不存在的事件"""
        response = client.get("/api/events/不存在的事件")
        assert response.status_code == 404
    
    def test_delete_nonexistent_event(self, client):
        """测试删除不存在的事件"""
        response = client.delete("/api/events/不存在的事件")
        assert response.status_code == 404


class TestFiltering:
    """筛选功能测试"""
    
    def test_filter_by_status(self, client):
        """测试按状态筛选"""
        tomorrow = date.today() + timedelta(days=1)
        yesterday = date.today() - timedelta(days=1)
        
        client.post("/api/events", json={"name": "未来", "date": tomorrow.isoformat()})
        client.post("/api/events", json={"name": "过去", "date": yesterday.isoformat()})
        
        # 筛选活跃事件
        response = client.get("/api/events?status=ACTIVE")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["events"][0]["name"] == "未来"
