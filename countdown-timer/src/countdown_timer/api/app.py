"""FastAPI 应用主入口"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .routes import router as api_router

# 创建 FastAPI 应用
app = FastAPI(
    title="Event Countdown API",
    description="事件倒计时工具 API v0.2.0",
    version="0.2.0",
)

# 注册 API 路由
app.include_router(api_router, prefix="/api")

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# 挂载静态文件
static_dir = BASE_DIR / "src" / "countdown_timer" / "web" / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", tags=["Web"])
async def root():
    """返回主页"""
    templates_dir = BASE_DIR / "src" / "countdown_timer" / "web" / "templates"
    index_file = templates_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")
    return {"message": "Event Countdown Tool v0.2.0"}


@app.get("/health", tags=["Health"])
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "version": "0.2.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
