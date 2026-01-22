"""Unit tests for Storage module."""

import pytest
from datetime import date, datetime, timedelta
from src.countdown_timer.storage import Storage


class TestStorageBasics:
    """Test basic storage operations."""

    @pytest.mark.unit
    def test_load_empty_storage(self, storage):
        """Loading from non-existent file should return empty dict."""
        events = storage.load_events()
        assert events == {}

    @pytest.mark.unit
    def test_event_exists_empty(self, storage):
        """Event should not exist in empty storage."""
        assert not storage.event_exists("生日")


class TestCreateEvent:
    """Test event creation (FR-001)."""

    @pytest.mark.unit
    def test_add_single_event(self, storage):
        """Adding event should create it in storage."""
        event = storage.add_event("生日", "2026-03-15")
        
        assert event["name"] == "生日"
        assert event["target_date"] == "2026-03-15"
        assert event["status"] in ["ACTIVE", "CURRENT", "EXPIRED"]
        
        # Verify it was saved
        assert storage.event_exists("生日")

    @pytest.mark.unit
    def test_add_duplicate_event_fails(self, storage):
        """Adding duplicate event should raise ValueError."""
        storage.add_event("生日", "2026-03-15")
        
        with pytest.raises(ValueError, match="already exists"):
            storage.add_event("生日", "2026-04-10")


class TestRemainingDays:
    """Test remaining days calculation (FR-002)."""

    @pytest.mark.unit
    def test_calculate_remaining_days(self):
        """Calculate remaining days correctly."""
        today = date.today()
        target = today + timedelta(days=10)
        target_str = target.isoformat()
        
        remaining = Storage._calculate_remaining_days(target_str)
        assert remaining == 10

    @pytest.mark.unit
    def test_remaining_days_today(self):
        """Same day should show 0 days (FR-006)."""
        today = date.today()
        target_str = today.isoformat()
        
        remaining = Storage._calculate_remaining_days(target_str)
        assert remaining == 0

    @pytest.mark.unit
    def test_remaining_days_past(self):
        """Past date should show 0 days, not negative (FR-006)."""
        yesterday = date.today() - timedelta(days=1)
        target_str = yesterday.isoformat()
        
        remaining = Storage._calculate_remaining_days(target_str)
        assert remaining == 0  # Never negative


class TestEventStatus:
    """Test event status calculation (FR-008b)."""

    @pytest.mark.unit
    def test_status_active(self):
        """Event in future should have ACTIVE status."""
        future = date.today() + timedelta(days=10)
        status = Storage._calculate_status(future.isoformat())
        assert status == "ACTIVE"

    @pytest.mark.unit
    def test_status_current(self):
        """Event today should have CURRENT status."""
        today = date.today()
        status = Storage._calculate_status(today.isoformat())
        assert status == "CURRENT"

    @pytest.mark.unit
    def test_status_expired(self):
        """Event in past should have EXPIRED status."""
        yesterday = date.today() - timedelta(days=1)
        status = Storage._calculate_status(yesterday.isoformat())
        assert status == "EXPIRED"


class TestQueryEvents:
    """Test querying events (FR-003)."""

    @pytest.mark.unit
    def test_get_event_by_name(self, storage):
        """Getting event by name should return event data."""
        storage.add_event("生日", "2026-03-15")
        
        event = storage.get_event("生日")
        assert event is not None
        assert event["name"] == "生日"
        assert "remaining_days" in event

    @pytest.mark.unit
    def test_get_nonexistent_event(self, storage):
        """Getting non-existent event should return None."""
        event = storage.get_event("不存在")
        assert event is None

    @pytest.mark.unit
    def test_get_all_events(self, storage):
        """Getting all events should return list with all events."""
        storage.add_event("生日", "2026-03-15")
        storage.add_event("假期", "2026-02-01")
        
        events = storage.get_all_events()
        assert len(events) == 2
        names = [e["name"] for e in events]
        assert "生日" in names
        assert "假期" in names


class TestDeleteEvent:
    """Test event deletion (FR-004)."""

    @pytest.mark.unit
    def test_delete_existing_event(self, storage):
        """Deleting existing event should remove it."""
        storage.add_event("生日", "2026-03-15")
        
        assert storage.delete_event("生日")
        assert not storage.event_exists("生日")

    @pytest.mark.unit
    def test_delete_nonexistent_event(self, storage):
        """Deleting non-existent event should return False."""
        result = storage.delete_event("不存在")
        assert not result
