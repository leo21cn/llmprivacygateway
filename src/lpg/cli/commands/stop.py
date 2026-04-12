"""Stop command."""

import click
from rich.console import Console

console = Console()


@click.command()
@click.option("-f", "--force", is_flag=True, help="强制停止")
@click.pass_context
def stop(ctx, force):
    """停止代理服务器."""
    facade = ctx.obj["facade"]

    try:
        facade.stop_service(force=force)
        console.print("[green]代理服务器已停止[/green]")
    except Exception as e:
        console.print(f"[red]停止失败: {e}[/red]")
        raise SystemExit(1)
