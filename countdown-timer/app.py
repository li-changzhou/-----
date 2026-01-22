#!/usr/bin/env python
"""
Event Countdown Tool - Web 服务器启动脚本

使用方法:
    python app.py                  # 在 localhost:8000 启动
    python app.py --host 0.0.0.0  # 允许外部访问
    python app.py --port 8080     # 使用不同端口
"""

import uvicorn
import argparse
from src.countdown_timer.api.app import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Event Countdown Tool - Web Server"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="服务器绑定的主机地址 (默认: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服务器绑定的端口 (默认: 8000)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="启用代码变更自动重载 (开发模式)",
    )
    
    args = parser.parse_args()
    
    print(f"🚀 启动 Event Countdown Tool Web 服务器...")
    print(f"📍 访问地址: http://{args.host}:{args.port}")
    print(f"📚 API 文档: http://{args.host}:{args.port}/docs")
    print(f"⏸️  按 Ctrl+C 停止服务器\n")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )
