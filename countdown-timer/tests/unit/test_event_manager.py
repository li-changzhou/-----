"""Unit tests for EventManager module."""

import pytest
from datetime import date, timedelta
from src.countdown_timer.event_manager import EventManager
from src.countdown_timer.validator import Validator


class TestEventManagerCreate:
    """Test event creation through manager."""

    @pytest.mark.unit
    def test_create_event(self, event_manager):
        """Creating event through manager should validate and store."""
        event = event_manager.create_event("生日", "2026-03-15")
        
        assert event["name"] == "生日"
        assert event["target_date"] == "2026-03-15"

    @pytest.mark.unit
    def test_create_invalid_name(self, event_manager):
        """Creating event with invalid name should raise error."""
        with pytest.raises(ValueError):
            event_manager.create_event("a" * 300, "2026-03-15")  # Too long

    @pytest.mark.unit
    def test_create_invalid_date_format(self, event_manager):
        """Creating event with invalid date format should raise error."""
        with pytest.raises(ValueError, match=".*date format.*"):
            event_manager.create_event("生日", "2026/03/15")

    @pytest.mark.unit
    def test_create_invalid_date_value(self, event_manager):
        """Creating event with invalid date should raise error."""
        with pytest.raises(ValueError):
            event_manager.create_event("生日", "2026-02-30")  # Invalid date

    @pytest.mark.unit
    def test_create_duplicate_event(self, event_manager):
        """Creating duplicate event should raise error (FR-008a)."""
        event_manager.create_event("生日", "2026-03-15")
        
        with pytest.raises(ValueError, match="already exists"):
            event_manager.create_event("生日", "2026-04-10")


class TestEventManagerQuery:
    """Test querying events."""

    @pytest.mark.unit
    def test_get_event(self, event_manager, sample_event):
        """Getting existing event should return event data."""
        event_manager.create_event(sample_event["name"], sample_event["target_date"])
        
        event = event_manager.get_event(sample_event["name"])
        assert event is not None
        assert event["name"] == sample_event["name"]

    @pytest.mark.unit
    def test_get_nonexistent_event(self, event_manager):
        """Getting non-existent event should return None."""
        event = event_manager.get_event("不存在")
        assert event is None

    @pytest.mark.unit
    def test_list_events_empty(self, event_manager):
        """Listing events from empty storage should return empty list."""
        events = event_manager.list_events()
        assert events == []

    @pytest.mark.unit
    def test_list_events_multiple(self, event_manager):
        """Listing multiple events should return all events."""
        event_manager.create_event("生日", "2026-03-15")
        event_manager.create_event("假期", "2026-02-01")
        event_manager.create_event("会议", "2026-05-20")
        
        events = event_manager.list_events()
        assert len(events) == 3
        names = [e["name"] for e in events]
        assert set(names) == {"生日", "假期", "会议"}


class TestEventManagerDelete:
    """Test event deletion."""

    @pytest.mark.unit
    def test_delete_event(self, event_manager, sample_event):
        """Deleting existing event should remove it."""
        event_manager.create_event(sample_event["name"], sample_event["target_date"])
        
        result = event_manager.delete_event(sample_event["name"])
        assert result is True
        
        # Verify it's gone
        event = event_manager.get_event(sample_event["name"])
        assert event is None

    @pytest.mark.unit
    def test_delete_nonexistent_event(self, event_manager):
        """Deleting non-existent event should return False."""
        result = event_manager.delete_event("不存在")
        assert result is False


class TestEventManagerFilter:
    """Test filtering events by status."""

    @pytest.mark.unit
    def test_get_events_by_status_active(self, event_manager):
        """Getting ACTIVE events should return future events."""
        future = date.today() + timedelta(days=10)
        event_manager.create_event("未来", future.isoformat())
        
        events = event_manager.get_event_by_status("ACTIVE")
        assert len(events) >= 1
        assert any(e["name"] == "未来" for e in events)

    @pytest.mark.unit
    def test_get_events_by_status_current(self, event_manager):
        """Getting CURRENT events should return today events."""
        today = date.today()
        event_manager.create_event("今天", today.isoformat())
        
        events = event_manager.get_event_by_status("CURRENT")
        assert len(events) >= 1
        assert any(e["name"] == "今天" for e in events)

    @pytest.mark.unit
    def test_get_events_by_status_expired(self, event_manager):
        """Getting EXPIRED events should return past events."""
        yesterday = date.today() - timedelta(days=1)
        event_manager.create_event("过期", yesterday.isoformat())
        
        events = event_manager.get_event_by_status("EXPIRED")
        assert len(events) >= 1
        assert any(e["name"] == "过期" for e in events)

    @pytest.mark.unit
    def test_get_events_empty_status(self, event_manager):
        """Getting events with non-matching status should return empty list."""
        events = event_manager.get_event_by_status("NONEXISTENT")
        assert events == []
