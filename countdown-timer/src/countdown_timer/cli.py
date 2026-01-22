"""CLI module - Command-line interface for P1."""

import click
from .event_manager import EventManager
from .storage import Storage
from .formatter import Formatter


@click.group()
def cli():
    """事件倒计时工具 - 管理重要日期的倒计时。"""
    pass


@cli.command()
@click.argument("name")
@click.argument("date")
def add(name: str, date: str):
    """创建新事件。
    
    示例: countdown add "生日" 2026-03-15
    """
    try:
        manager = EventManager()
        event = manager.create_event(name, date)
        remaining = event["remaining_days"]
        message = Formatter.format_success(f"{name} 已创建，还有 {remaining} 天")
        click.echo(message)
    except ValueError as e:
        click.echo(Formatter.format_error(str(e)), err=True)
        raise SystemExit(1)


@cli.command()
def list():
    """列出所有事件。"""
    try:
        manager = EventManager()
        events = manager.list_events()
        
        if not events:
            click.echo("暂无事件")
        else:
            click.echo(Formatter.format_events_list(events))
    except Exception as e:
        click.echo(Formatter.format_error(str(e)), err=True)
        raise SystemExit(1)


@cli.command()
@click.argument("name")
def delete(name: str):
    """删除事件。
    
    示例: countdown delete "生日"
    """
    try:
        manager = EventManager()
        if manager.delete_event(name):
            message = Formatter.format_success(f"{name} 已删除")
            click.echo(message)
        else:
            click.echo(Formatter.format_error(f"事件 '{name}' 不存在"), err=True)
            raise SystemExit(1)
    except Exception as e:
        click.echo(Formatter.format_error(str(e)), err=True)
        raise SystemExit(1)


@cli.command()
@click.argument("name")
def show(name: str):
    """显示单个事件详情。
    
    示例: countdown show "生日"
    """
    try:
        manager = EventManager()
        event = manager.get_event(name)
        
        if event is None:
            click.echo(Formatter.format_error(f"事件 '{name}' 不存在"), err=True)
            raise SystemExit(1)
        
        formatted = Formatter.format_event_for_cli(event)
        click.echo(formatted)
    except Exception as e:
        click.echo(Formatter.format_error(str(e)), err=True)
        raise SystemExit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
