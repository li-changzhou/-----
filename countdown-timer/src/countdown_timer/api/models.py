"""Pydantic 数据模型定义"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class EventBase(BaseModel):
    """事件基础数据模型"""
    name: str = Field(..., min_length=1, max_length=256, description="事件名称")
    date: date = Field(..., description="事件日期 (YYYY-MM-DD)")


class EventCreate(EventBase):
    """创建事件请求模型"""
    pass


class EventUpdate(BaseModel):
    """更新事件请求模型"""
    date: Optional[date] = Field(None, description="新的事件日期")


class Event(EventBase):
    """事件响应模型"""
    status: str = Field(..., description="事件状态: ACTIVE/CURRENT/EXPIRED")
    days_remaining: int = Field(..., ge=0, description="剩余天数")

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """事件列表响应模型"""
    events: list[Event] = Field(..., description="事件列表")
    total: int = Field(..., ge=0, description="事件总数")


class StatsResponse(BaseModel):
    """统计数据响应模型"""
    total_events: int = Field(..., ge=0, description="总事件数")
    active_events: int = Field(..., ge=0, description="进行中事件")
    expired_events: int = Field(..., ge=0, description="已过期事件")
    next_event: Optional[str] = Field(None, description="下一个事件名称")
    next_event_days: Optional[int] = Field(None, description="下一个事件剩余天数")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    detail: str = Field(..., description="错误详情")
    code: str = Field(..., description="错误代码")
