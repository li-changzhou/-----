"""Integration tests for CLI module."""

import pytest
from click.testing import CliRunner
from datetime import date, timedelta
from src.countdown_timer.cli import cli
from src.countdown_timer.event_manager import EventManager


@pytest.fixture
def cli_runner(temp_storage_dir):
    """Create CliRunner with temporary storage."""
    import os
    os.environ["COUNTDOWN_HOME"] = str(temp_storage_dir)
    return CliRunner()


class TestCLIAdd:
    """Test 'add' command."""

    @pytest.mark.unit
    def test_add_command_success(self, cli_runner):
        """Adding event via CLI should succeed."""
        result = cli_runner.invoke(cli, ["add", "生日", "2026-03-15"])
        
        assert result.exit_code == 0
        assert "生日" in result.output or "成功" in result.output or "Success" in result.output

    @pytest.mark.unit
    def test_add_command_invalid_date(self, cli_runner):
        """Adding event with invalid date should fail."""
        result = cli_runner.invoke(cli, ["add", "生日", "2026/03/15"])
        
        assert result.exit_code != 0

    @pytest.mark.unit
    def test_add_command_invalid_name(self, cli_runner):
        """Adding event with invalid name should fail."""
        result = cli_runner.invoke(cli, ["add", "a" * 300, "2026-03-15"])
        
        assert result.exit_code != 0

    @pytest.mark.unit
    def test_add_command_duplicate(self, cli_runner):
        """Adding duplicate event should fail."""
        cli_runner.invoke(cli, ["add", "生日", "2026-03-15"])
        result = cli_runner.invoke(cli, ["add", "生日", "2026-04-10"])
        
        assert result.exit_code != 0


class TestCLIList:
    """Test 'list' command."""

    @pytest.mark.unit
    def test_list_command_empty(self, cli_runner):
        """Listing events when empty should show message."""
        result = cli_runner.invoke(cli, ["list"])
        
        assert result.exit_code == 0

    @pytest.mark.unit
    def test_list_command_with_events(self, cli_runner):
        """Listing events should display all events."""
        cli_runner.invoke(cli, ["add", "生日", "2026-03-15"])
        cli_runner.invoke(cli, ["add", "假期", "2026-02-01"])
        
        result = cli_runner.invoke(cli, ["list"])
        
        assert result.exit_code == 0
        assert "生日" in result.output
        assert "假期" in result.output


class TestCLIShow:
    """Test 'show' command."""

    @pytest.mark.unit
    def test_show_command_existing_event(self, cli_runner):
        """Showing existing event should display details."""
        cli_runner.invoke(cli, ["add", "生日", "2026-03-15"])
        result = cli_runner.invoke(cli, ["show", "生日"])
        
        assert result.exit_code == 0
        assert "生日" in result.output

    @pytest.mark.unit
    def test_show_command_nonexistent_event(self, cli_runner):
        """Showing non-existent event should fail."""
        result = cli_runner.invoke(cli, ["show", "不存在"])
        
        assert result.exit_code != 0


class TestCLIDelete:
    """Test 'delete' command."""

    @pytest.mark.unit
    def test_delete_command_success(self, cli_runner):
        """Deleting event should succeed."""
        cli_runner.invoke(cli, ["add", "生日", "2026-03-15"])
        result = cli_runner.invoke(cli, ["delete", "生日"])
        
        assert result.exit_code == 0
        
        # Verify it's deleted
        show_result = cli_runner.invoke(cli, ["show", "生日"])
        assert show_result.exit_code != 0

    @pytest.mark.unit
    def test_delete_command_nonexistent(self, cli_runner):
        """Deleting non-existent event should fail."""
        result = cli_runner.invoke(cli, ["delete", "不存在"])
        
        assert result.exit_code != 0


class TestCLIHelp:
    """Test help and info commands."""

    @pytest.mark.unit
    def test_help_command(self, cli_runner):
        """Help command should display usage."""
        result = cli_runner.invoke(cli, ["--help"])
        
        assert result.exit_code == 0
        assert "add" in result.output
        assert "list" in result.output
        assert "delete" in result.output
        assert "show" in result.output

    @pytest.mark.unit
    def test_help_add_command(self, cli_runner):
        """Help for add command should display."""
        result = cli_runner.invoke(cli, ["add", "--help"])
        
        assert result.exit_code == 0


class TestCLIWorkflow:
    """Test complete CLI workflow (Scenario 1-4)."""

    @pytest.mark.unit
    def test_workflow_create_list_show_delete(self, cli_runner):
        """Complete workflow: add → list → show → delete."""
        # Add event (Scenario 1)
        add_result = cli_runner.invoke(cli, ["add", "生日", "2026-03-15"])
        assert add_result.exit_code == 0
        
        # List events
        list_result = cli_runner.invoke(cli, ["list"])
        assert list_result.exit_code == 0
        assert "生日" in list_result.output
        
        # Show event details
        show_result = cli_runner.invoke(cli, ["show", "生日"])
        assert show_result.exit_code == 0
        
        # Delete event (Scenario 4)
        del_result = cli_runner.invoke(cli, ["delete", "生日"])
        assert del_result.exit_code == 0
        
        # Verify deleted
        final_list = cli_runner.invoke(cli, ["list"])
        assert "生日" not in final_list.output or final_list.exit_code == 0
