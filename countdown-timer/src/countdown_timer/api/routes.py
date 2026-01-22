"""API 路由定义"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, date
from typing import Optional

from ..event_manager import EventManager
from ..storage import EventStorage
from .models import (
    Event,
    EventCreate,
    EventUpdate,
    EventListResponse,
    StatsResponse,
    ErrorResponse,
)

router = APIRouter(tags=["Events"])

# 初始化存储和管理器
storage = EventStorage()
manager = EventManager(storage)


@router.get("/events", response_model=EventListResponse, summary="获取所有事件")
async def list_events(
    status: Optional[str] = Query(None, description="筛选状态: ACTIVE/CURRENT/EXPIRED")
):
    """获取所有事件，可按状态筛选"""
    try:
        all_events = manager.list_events()
        
        # 如果指定了状态筛选
        if status:
            all_events = [e for e in all_events if e.get("status") == status]
        
        # 转换为 API 响应格式
        events = [
            Event(
                name=e["name"],
                date=datetime.strptime(e["date"], "%Y-%m-%d").date(),
                status=e.get("status", "ACTIVE"),
                days_remaining=e.get("days_remaining", 0),
            )
            for e in all_events
        ]
        
        return EventListResponse(events=events, total=len(events))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取事件失败: {str(e)}")


@router.post("/events", response_model=Event, status_code=201, summary="创建新事件")
async def create_event(event: EventCreate):
    """创建一个新的倒计时事件"""
    try:
        # 验证并创建事件
        result = manager.create_event(
            event.name,
            event.date.strftime("%Y-%m-%d")
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "创建事件失败")
            )
        
        event_data = result.get("event", {})
        return Event(
            name=event_data["name"],
            date=event.date,
            status=event_data.get("status", "ACTIVE"),
            days_remaining=event_data.get("days_remaining", 0),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建事件失败: {str(e)}")


@router.get("/events/{name}", response_model=Event, summary="获取事件详情")
async def get_event(name: str):
    """获取指定事件的详细信息"""
    try:
        event_data = manager.get_event(name)
        
        if not event_data:
            raise HTTPException(
                status_code=404,
                detail=f"事件 '{name}' 不存在"
            )
        
        return Event(
            name=event_data["name"],
            date=datetime.strptime(event_data["date"], "%Y-%m-%d").date(),
            status=event_data.get("status", "ACTIVE"),
            days_remaining=event_data.get("days_remaining", 0),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取事件失败: {str(e)}")


@router.put("/events/{name}", response_model=Event, summary="更新事件")
async def update_event(name: str, event: EventUpdate):
    """更新指定事件"""
    try:
        # 首先检查事件是否存在
        existing = manager.get_event(name)
        if not existing:
            raise HTTPException(
                status_code=404,
                detail=f"事件 '{name}' 不存在"
            )
        
        # 删除旧事件
        delete_result = manager.delete_event(name)
        if not delete_result.get("success"):
            raise HTTPException(status_code=400, detail="更新事件失败")
        
        # 创建新事件
        new_date = event.date if event.date else datetime.strptime(existing["date"], "%Y-%m-%d").date()
        create_result = manager.create_event(name, new_date.strftime("%Y-%m-%d"))
        
        if not create_result.get("success"):
            raise HTTPException(status_code=400, detail="更新事件失败")
        
        event_data = create_result.get("event", {})
        return Event(
            name=event_data["name"],
            date=new_date,
            status=event_data.get("status", "ACTIVE"),
            days_remaining=event_data.get("days_remaining", 0),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新事件失败: {str(e)}")


@router.delete("/events/{name}", status_code=204, summary="删除事件")
async def delete_event(name: str):
    """删除指定事件"""
    try:
        result = manager.delete_event(name)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=404,
                detail=f"事件 '{name}' 不存在"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除事件失败: {str(e)}")


@router.get("/stats", response_model=StatsResponse, summary="获取统计数据")
async def get_stats():
    """获取事件统计信息"""
    try:
        all_events = manager.list_events()
        
        total = len(all_events)
        active = len([e for e in all_events if e.get("status") == "ACTIVE"])
        expired = len([e for e in all_events if e.get("status") == "EXPIRED"])
        
        # 找下一个最近的事件
        next_event = None
        next_days = None
        active_events = [e for e in all_events if e.get("status") in ["ACTIVE", "CURRENT"]]
        if active_events:
            # 按剩余天数排序
            active_events.sort(key=lambda x: x.get("days_remaining", 0))
            next_event = active_events[0]["name"]
            next_days = active_events[0].get("days_remaining", 0)
        
        return StatsResponse(
            total_events=total,
            active_events=active,
            expired_events=expired,
            next_event=next_event,
            next_event_days=next_days,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")
