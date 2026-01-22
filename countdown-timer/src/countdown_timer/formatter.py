"""Formatter module - Output formatting (FR-007)."""

from typing import List, Dict


class Formatter:
    """Formats event data for display."""

    @staticmethod
    def format_event_for_cli(event: Dict) -> str:
        """
        Format single event for CLI display (FR-007).
        
        Format: "事件名 n 天"
        
        Args:
            event: Event dictionary
            
        Returns:
            Formatted string
        """
        name = event["name"]
        remaining = event.get("remaining_days", 0)
        status = event.get("status", "ACTIVE")
        
        if status == "EXPIRED":
            return f"{name} (已过期)"
        else:
            return f"{name} 还有 {remaining} 天"

    @staticmethod
    def format_events_list(events: List[Dict]) -> str:
        """
        Format events list for CLI display (FR-007).
        
        Args:
            events: List of events
            
        Returns:
            Formatted list string
        """
        if not events:
            return "暂无事件"
        
        lines = []
        for i, event in enumerate(events, 1):
            formatted = Formatter.format_event_for_cli(event)
            lines.append(f"{i}. {formatted}")
        
        return "\n".join(lines)

    @staticmethod
    def format_error(error: str) -> str:
        """
        Format error message for display.
        
        Args:
            error: Error message
            
        Returns:
            Formatted error string
        """
        return f"❌ 错误: {error}"

    @staticmethod
    def format_success(message: str) -> str:
        """
        Format success message for display.
        
        Args:
            message: Success message
            
        Returns:
            Formatted success string
        """
        return f"✅ {message}"
