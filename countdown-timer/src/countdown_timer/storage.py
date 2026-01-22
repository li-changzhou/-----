"""Storage module - Event data persistence (P1: JSON)."""

import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Optional, List


class Storage:
    """Manages event data storage (JSON for P1)."""

    def __init__(self, storage_dir: Optional[str] = None):
        """
        Initialize storage.
        
        Args:
            storage_dir: Directory for storing events.json. 
                        Defaults to ~/.countdown
        """
        if storage_dir is None:
            storage_dir = os.path.expanduser("~/.countdown")
        
        self.storage_dir = Path(storage_dir)
        self.events_file = self.storage_dir / "events.json"
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def load_events(self) -> Dict:
        """
        Load all events from storage (FR-006).
        
        Returns:
            Dictionary of events {name: event_data}
            
        Returns empty dict if file doesn't exist.
        """
        if not self.events_file.exists():
            return {}
        
        with open(self.events_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save_events(self, events: Dict) -> None:
        """
        Save events to storage (NFR-006: persistence).
        
        Args:
            events: Dictionary of events to save
        """
        with open(self.events_file, "w") as f:
            json.dump(events, f, indent=2)

    def event_exists(self, name: str) -> bool:
        """
        Check if event with given name exists (FR-008a: reject duplicates).
        
        Args:
            name: Event name to check
            
        Returns:
            True if event exists, False otherwise
        """
        events = self.load_events()
        return name in events

    def add_event(self, name: str, target_date: str) -> Dict:
        """
        Add new event to storage (FR-001: create event).
        
        Args:
            name: Event name (unique)
            target_date: Target date (YYYY-MM-DD)
            
        Returns:
            Created event data
            
        Raises:
            ValueError: If event already exists
        """
        if self.event_exists(name):
            raise ValueError(f"Event '{name}' already exists")
        
        events = self.load_events()
        event_data = {
            "name": name,
            "target_date": target_date,
            "created_at": datetime.now().isoformat(),
            "status": self._calculate_status(target_date),
        }
        
        events[name] = event_data
        self.save_events(events)
        
        return event_data

    def get_event(self, name: str) -> Optional[Dict]:
        """
        Get single event (FR-003: query event).
        
        Args:
            name: Event name
            
        Returns:
            Event data with remaining_days, or None if not found
        """
        events = self.load_events()
        if name not in events:
            return None
        
        event = events[name]
        event["remaining_days"] = self._calculate_remaining_days(event["target_date"])
        event["status"] = self._calculate_status(event["target_date"])
        
        return event

    def get_all_events(self) -> List[Dict]:
        """
        Get all events (FR-003: query all events).
        
        Returns:
            List of all events with remaining_days calculated
        """
        events = self.load_events()
        result = []
        
        for name, event_data in events.items():
            event = event_data.copy()
            event["remaining_days"] = self._calculate_remaining_days(event["target_date"])
            event["status"] = self._calculate_status(event["target_date"])
            result.append(event)
        
        return result

    def delete_event(self, name: str) -> bool:
        """
        Delete event (FR-004: delete event).
        
        Args:
            name: Event name to delete
            
        Returns:
            True if deleted, False if not found
        """
        events = self.load_events()
        if name not in events:
            return False
        
        del events[name]
        self.save_events(events)
        
        return True

    @staticmethod
    def _calculate_remaining_days(target_date_str: str) -> int:
        """
        Calculate remaining days (FR-002: daily calculation).
        
        Args:
            target_date_str: Target date (YYYY-MM-DD)
            
        Returns:
            Remaining days (0 if today or past, not negative)
        """
        today = date.today()
        target = datetime.fromisoformat(target_date_str).date()
        remaining = (target - today).days
        
        # FR-006: Never return negative, display 0 for today onwards
        return max(0, remaining)

    @staticmethod
    def _calculate_status(target_date_str: str) -> str:
        """
        Calculate event status (FR-008b: state transitions).
        
        States:
        - ACTIVE: remaining_days > 0
        - CURRENT: remaining_days = 0
        - EXPIRED: remaining_days was < 0 (but we show as CURRENT)
        
        Args:
            target_date_str: Target date (YYYY-MM-DD)
            
        Returns:
            Event status
        """
        today = date.today()
        target = datetime.fromisoformat(target_date_str).date()
        remaining = (target - today).days
        
        if remaining > 0:
            return "ACTIVE"
        elif remaining == 0:
            return "CURRENT"
        else:
            return "EXPIRED"
