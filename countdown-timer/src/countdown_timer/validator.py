"""Validator module - Input validation for events."""

from datetime import datetime, date


class Validator:
    """Validates event input data."""

    @staticmethod
    def validate_date_format(date_string: str) -> bool:
        """
        Validate date format (YYYY-MM-DD).
        
        Args:
            date_string: Date string to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError as e:
            raise ValueError(f"Invalid date format: {date_string}. Expected YYYY-MM-DD") from e

    @staticmethod
    def validate_date_value(date_string: str) -> bool:
        """
        Validate that date is a valid calendar date.
        
        Args:
            date_string: Date string to validate (YYYY-MM-DD)
            
        Returns:
            True if valid date
            
        Raises:
            ValueError: If date is invalid (e.g., 2026-13-01)
        """
        try:
            datetime.strptime(date_string, "%Y-%m-%d").date()
            return True
        except ValueError as e:
            raise ValueError(f"Invalid calendar date: {date_string}") from e

    @staticmethod
    def validate_event_name(name: str) -> bool:
        """
        Validate event name (FR-008c).
        
        Rules:
        - Non-empty
        - Max 256 characters
        - No tabs or newlines
        
        Args:
            name: Event name to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If name is invalid
        """
        if not name:
            raise ValueError("Event name cannot be empty")
        
        if len(name) > 256:
            raise ValueError(f"Event name too long: {len(name)} > 256")
        
        if "\t" in name or "\n" in name:
            raise ValueError("Event name cannot contain tabs or newlines")
        
        return True

    @staticmethod
    def validate_event(name: str, target_date_str: str) -> bool:
        """
        Validate complete event data (FR-005).
        
        Args:
            name: Event name
            target_date_str: Target date (YYYY-MM-DD)
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If any validation fails
        """
        Validator.validate_event_name(name)
        Validator.validate_date_format(target_date_str)
        Validator.validate_date_value(target_date_str)
        return True
