"""Unit tests for Validator module."""

import pytest
from datetime import datetime
from src.countdown_timer.validator import Validator


class TestValidateDateFormat:
    """Test date format validation (FR-005)."""

    @pytest.mark.unit
    def test_valid_date_format(self):
        """Valid date format should pass."""
        assert Validator.validate_date_format("2026-03-15")
        assert Validator.validate_date_format("2026-01-01")
        assert Validator.validate_date_format("2126-12-31")

    @pytest.mark.unit
    def test_invalid_date_format(self):
        """Invalid date formats should raise ValueError."""
        with pytest.raises(ValueError, match=".*date format.*"):
            Validator.validate_date_format("not-a-date")
        
        with pytest.raises(ValueError):
            Validator.validate_date_format("15-03-2026")
        
        with pytest.raises(ValueError):
            Validator.validate_date_format("abc")


class TestValidateDateValue:
    """Test date value validation (FR-005)."""

    @pytest.mark.unit
    def test_valid_date_value(self):
        """Valid calendar dates should pass."""
        assert Validator.validate_date_value("2026-03-15")
        assert Validator.validate_date_value("2026-02-28")
        assert Validator.validate_date_value("2024-02-29")  # Leap year

    @pytest.mark.unit
    def test_invalid_date_value(self):
        """Invalid calendar dates should raise ValueError."""
        with pytest.raises(ValueError):
            Validator.validate_date_value("2026-13-01")  # Month 13
        
        with pytest.raises(ValueError):
            Validator.validate_date_value("2026-02-30")  # No Feb 30


class TestValidateEventName:
    """Test event name validation (FR-008c)."""

    @pytest.mark.unit
    def test_valid_name(self):
        """Valid names should pass."""
        assert Validator.validate_event_name("生日")
        assert Validator.validate_event_name("My Birthday")
        assert Validator.validate_event_name("a" * 256)  # Max length

    @pytest.mark.unit
    def test_empty_name(self):
        """Empty name should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Validator.validate_event_name("")

    @pytest.mark.unit
    def test_name_too_long(self):
        """Names > 256 chars should raise ValueError."""
        with pytest.raises(ValueError, match="too long"):
            Validator.validate_event_name("a" * 257)

    @pytest.mark.unit
    def test_name_with_tab(self):
        """Names with tabs should raise ValueError."""
        with pytest.raises(ValueError, match="cannot contain"):
            Validator.validate_event_name("生日\t备忘")

    @pytest.mark.unit
    def test_name_with_newline(self):
        """Names with newlines should raise ValueError."""
        with pytest.raises(ValueError, match="cannot contain"):
            Validator.validate_event_name("生日\n备忘")


class TestValidateEvent:
    """Test complete event validation."""

    @pytest.mark.unit
    def test_valid_event(self):
        """Valid event data should pass all validations."""
        assert Validator.validate_event("生日", "2026-03-15")
        assert Validator.validate_event("My Event", "2026-12-31")

    @pytest.mark.unit
    def test_invalid_event_name(self):
        """Invalid event name should raise ValueError."""
        with pytest.raises(ValueError):
            Validator.validate_event("", "2026-03-15")

    @pytest.mark.unit
    def test_invalid_event_date(self):
        """Invalid date should raise ValueError."""
        with pytest.raises(ValueError):
            Validator.validate_event("生日", "invalid")
        
        with pytest.raises(ValueError):
            Validator.validate_event("生日", "2026-13-01")
