"""Event Manager module - Business logic."""

from typing import List, Dict, Optional
from .validator import Validator
from .storage import Storage


class EventManager:
    """Manages events business logic."""

    def __init__(self, storage: Optional[Storage] = None):
        """
        Initialize Event Manager.
        
        Args:
            storage: Storage instance. Defaults to Storage()
        """
        self.storage = storage or Storage()
        self.validator = Validator()

    def create_event(self, name: str, target_date: str) -> Dict:
        """
        Create new event (FR-001, FR-008a).
        
        Args:
            name: Event name (unique, max 256 chars)
            target_date: Target date (YYYY-MM-DD)
            
        Returns:
            Created event data with remaining_days
            
        Raises:
            ValueError: If validation fails or event exists
        """
        # Validate input (FR-005)
        self.validator.validate_event(name, target_date)
        
        # Check for duplicates (FR-008a)
        if self.storage.event_exists(name):
            raise ValueError(f"Event '{name}' already exists, please use a different name")
        
        # Create and return
        event = self.storage.add_event(name, target_date)
        event["remaining_days"] = self.storage._calculate_remaining_days(target_date)
        
        return event

    def get_event(self, name: str) -> Optional[Dict]:
        """
        Get event by name (FR-003).
        
        Args:
            name: Event name
            
        Returns:
            Event data with remaining_days, or None if not found
        """
        return self.storage.get_event(name)

    def list_events(self) -> List[Dict]:
        """
        List all events (FR-003).
        
        Returns:
            List of all events with remaining_days
        """
        return self.storage.get_all_events()

    def delete_event(self, name: str) -> bool:
        """
        Delete event (FR-004).
        
        Args:
            name: Event name
            
        Returns:
            True if deleted, False if not found
        """
        return self.storage.delete_event(name)

    def get_event_by_status(self, status: str) -> List[Dict]:
        """
        Get events filtered by status (FR-008b).
        
        Args:
            status: Status to filter (ACTIVE/CURRENT/EXPIRED)
            
        Returns:
            List of events with matching status
        """
        all_events = self.list_events()
        return [e for e in all_events if e["status"] == status]
