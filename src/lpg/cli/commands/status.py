"""Status command."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.command()
@click.option("-j", "--json", "json_output", is_flag=True, help="JSON 格式输出")
@click.pass_context
def status(ctx, json_output):
    """查看服务状态."""
    facade = ctx.obj["facade"]
    status_info = facade.get_status()

    if json_output:
        import json

        click.echo(json.dumps(status_info, indent=2, ensure_ascii=False))
        return

    if status_info["running"]:
        console.print(
            f"""
┌─────────────────────────────────────────────────────────────┐
│  LLM Privacy Gateway Status                                 │
├─────────────────────────────────────────────────────────────┤
│  Status:       ● Running                                    │
│  Uptime:       {status_info['uptime']:.0f}s                                   │
│  Port:         {status_info['port']}                                        │
│  PID:          {status_info['pid']}                                         │
├─────────────────────────────────────────────────────────────┤
│  Active Keys:      {status_info['keys_count']}                                        │
│  Rules Loaded:     {status_info['rules_count']}                                       │
└─────────────────────────────────────────────────────────────┘
"""
        )
    else:
        console.print(
            """
┌─────────────────────────────────────────────────────────────┐
│  LLM Privacy Gateway Status                                 │
├─────────────────────────────────────────────────────────────┤
│  Status:       ○ Stopped                                    │
└─────────────────────────────────────────────────────────────┘
"""
        )
