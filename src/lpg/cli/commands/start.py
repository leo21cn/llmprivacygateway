"""Start command."""

import click
from rich.console import Console

console = Console()


@click.command()
@click.option("-p", "--port", default=8080, help="代理端口")
@click.option("-h", "--host", default="127.0.0.1", help="监听地址")
@click.option("-d", "--daemon", is_flag=True, help="后台运行模式")
@click.option(
    "--log-level",
    type=click.Choice(["debug", "info", "warn", "error"]),
    default="info",
    help="日志级别",
)
@click.option("--log-file", help="日志文件路径")
@click.pass_context
def start(ctx, port, host, daemon, log_level, log_file):
    """启动代理服务器."""
    facade = ctx.obj["facade"]

    if facade.is_running():
        console.print("[yellow]代理服务器已在运行[/yellow]")
        return

    try:
        facade.start_service(
            host=host,
            port=port,
            daemon=daemon,
            log_level=log_level,
            log_file=log_file,
        )
        _print_startup_info(facade)
    except Exception as e:
        console.print(f"[red]启动失败: {e}[/red]")
        raise SystemExit(1)


def _print_startup_info(facade):
    """打印启动信息."""
    status = facade.get_status()
    console.print(
        f"""
[bold green]╔═══════════════════════════════════════════════════════════╗
║         LLM Privacy Gateway v1.0.0                        ║
║         Your AI Privacy Shield                            ║
╚═══════════════════════════════════════════════════════════╝[/bold green]

  ✓ Configuration loaded
  ✓ Rules loaded: {status['rules_count']} active rules
  ✓ Virtual keys loaded: {status['keys_count']} active keys

  ┌─────────────────────────────────────────────────────────────┐
  │  Proxy Server Running                                       │
  │  ─────────────────────────────────────────────────────────  │
  │  Address:     http://{status['host']}:{status['port']}                         
  │  PID:         {status['pid']}                                         
  └─────────────────────────────────────────────────────────────┘

  Press Ctrl+C to stop
"""
    )
