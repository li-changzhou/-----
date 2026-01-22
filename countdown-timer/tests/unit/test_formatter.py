"""Unit tests for Formatter module."""

import pytest
from datetime import date, timedelta
from src.countdown_timer.formatter import Formatter


class TestFormatEvent:
    """Test event formatting (FR-007)."""

    @pytest.mark.unit
    def test_format_active_event(self):
        """Format ACTIVE event with remaining days."""
        event = {
            "name": "生日",
            "status": "ACTIVE",
            "remaining_days": 10
        }
        
        formatted = Formatter.format_event_for_cli(event)
        assert "生日" in formatted
        assert "10" in formatted or "10 天" in formatted

    @pytest.mark.unit
    def test_format_current_event(self):
        """Format CURRENT event (today) with 0 days."""
        event = {
            "name": "生日",
            "status": "CURRENT",
            "remaining_days": 0
        }
        
        formatted = Formatter.format_event_for_cli(event)
        assert "生日" in formatted
        # Should mention "today" or "0"
        assert "0" in formatted or "今" in formatted or "Today" in formatted

    @pytest.mark.unit
    def test_format_expired_event(self):
        """Format EXPIRED event."""
        event = {
            "name": "生日",
            "status": "EXPIRED",
            "remaining_days": 0
        }
        
        formatted = Formatter.format_event_for_cli(event)
        assert "生日" in formatted
        # Should indicate expired status
        assert "已过期" in formatted or "Expired" in formatted or "过期" in formatted

    @pytest.mark.unit
    def test_format_event_with_special_chars(self):
        """Format event name with special characters."""
        event = {
            "name": "会议/讲座",
            "status": "ACTIVE",
            "remaining_days": 5
        }
        
        formatted = Formatter.format_event_for_cli(event)
        assert "会议/讲座" in formatted


class TestFormatEventsList:
    """Test list formatting."""

    @pytest.mark.unit
    def test_format_empty_list(self):
        """Format empty event list."""
        formatted = Formatter.format_events_list([])
        assert formatted  # Should not be empty (should have message)

    @pytest.mark.unit
    def test_format_single_event_list(self):
        """Format list with single event."""
        events = [{
            "name": "生日",
            "status": "ACTIVE",
            "remaining_days": 10
        }]
        
        formatted = Formatter.format_events_list(events)
        assert "生日" in formatted

    @pytest.mark.unit
    def test_format_multiple_events_list(self):
        """Format list with multiple events."""
        events = [
            {
                "name": "生日",
                "status": "ACTIVE",
                "remaining_days": 10
            },
            {
                "name": "假期",
                "status": "ACTIVE",
                "remaining_days": 5
            }
        ]
        
        formatted = Formatter.format_events_list(events)
        assert "生日" in formatted
        assert "假期" in formatted


class TestFormatMessages:
    """Test error and success message formatting."""

    @pytest.mark.unit
    def test_format_error(self):
        """Format error message."""
        error_msg = "Event name is too long"
        formatted = Formatter.format_error(error_msg)
        
        assert error_msg in formatted or "错误" in formatted or "Error" in formatted

    @pytest.mark.unit
    def test_format_success_create(self):
        """Format success message for creation."""
        msg = "事件 生日 已创建"
        formatted = Formatter.format_success(msg)
        
        assert "生日" in formatted

    @pytest.mark.unit
    def test_format_success_delete(self):
        """Format success message for deletion."""
        msg = "事件 生日 已删除"
        formatted = Formatter.format_success(msg)
        
        assert "生日" in formatted
