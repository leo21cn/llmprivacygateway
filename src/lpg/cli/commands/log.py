"""Log command."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def log():
    """日志查看与分析."""
    pass


@log.command("show")
@click.option("-n", "--lines", default=50, help="显示行数")
@click.option("--since", help="时间范围 (1h/1d/1w)")
@click.option("-j", "--json", "json_output", is_flag=True, help="JSON 格式输出")
@click.pass_context
def show(ctx, lines, since, json_output):
    """显示日志."""
    facade = ctx.obj["facade"]
    logs = facade.get_logs(lines=lines, since=since)

    if json_output:
        import json

        click.echo(json.dumps(logs, indent=2, ensure_ascii=False))
        return

    if not logs:
        console.print("[yellow]暂无日志[/yellow]")
        return

    for entry in logs:
        console.print(f"[{entry['timestamp']}] {entry['method']} {entry['url']}")


@log.command("stats")
@click.option("--since", help="时间范围 (1h/1d/1w)")
@click.pass_context
def stats(ctx, since):
    """统计分析."""
    facade = ctx.obj["facade"]
    stats_info = facade.get_log_stats(since=since)

    console.print("\n[bold]请求统计[/bold]")
    console.print(f"  总请求数: {stats_info['total_requests']}")
    console.print(f"  成功请求: {stats_info['success_requests']}")
    console.print(f"  失败请求: {stats_info['failed_requests']}")
    console.print(f"  PII 检测: {stats_info['pii_detected']}")
    console.print(f"  平均耗时: {stats_info['avg_duration_ms']}ms")
