"""Conftest - Pytest configuration and fixtures."""

import pytest
import tempfile
from pathlib import Path
from src.countdown_timer.storage import Storage
from src.countdown_timer.event_manager import EventManager


@pytest.fixture
def temp_storage_dir():
    """Temporary directory for test storage."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def storage(temp_storage_dir):
    """Storage instance with temporary directory."""
    return Storage(storage_dir=temp_storage_dir)


@pytest.fixture
def event_manager(storage):
    """Event manager with temporary storage."""
    return EventManager(storage=storage)


@pytest.fixture
def sample_event():
    """Sample event data."""
    return {
        "name": "生日",
        "target_date": "2026-03-15",
    }
