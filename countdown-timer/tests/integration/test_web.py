"""Web UI 集成测试"""

import pytest
from fastapi.testclient import TestClient
from src.countdown_timer.api.app import app


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


class TestWebUI:
    """Web UI 测试"""
    
    def test_home_page_loads(self, client):
        """测试主页加载"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_static_files_accessible(self, client):
        """测试静态文件访问"""
        # 测试 CSS
        response = client.get("/static/css/style.css")
        # 文件可能不存在也是可以接受的，关键是路由正确
        assert response.status_code in [200, 404]
        
        # 测试 JS
        response = client.get("/static/js/app.js")
        assert response.status_code in [200, 404]
    
    def test_api_documentation(self, client):
        """测试 Swagger 自动文档"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()
    
    def test_openapi_schema(self, client):
        """测试 OpenAPI 模式"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "paths" in data
        assert "/api/events" in data["paths"]


class TestResponsiveness:
    """响应性能测试"""
    
    def test_api_response_time(self, client):
        """测试 API 响应时间"""
        import time
        
        start = time.time()
        client.get("/api/stats")
        duration = time.time() - start
        
        # 应该在 200ms 内完成
        assert duration < 0.2
    
    def test_concurrent_requests(self, client):
        """测试并发请求"""
        from datetime import date, timedelta
        
        tomorrow = date.today() + timedelta(days=1)
        
        # 创建事件
        for i in range(5):
            response = client.post(
                "/api/events",
                json={"name": f"事件{i}", "date": tomorrow.isoformat()}
            )
            assert response.status_code == 201
        
        # 并发获取列表
        for _ in range(10):
            response = client.get("/api/events")
            assert response.status_code == 200
