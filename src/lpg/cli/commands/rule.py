"""Rule command."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def rule():
    """规则管理."""
    pass


@rule.command("list")
@click.option("-c", "--category", help="规则分类")
@click.option("-j", "--json", "json_output", is_flag=True, help="JSON 格式输出")
@click.pass_context
def list_rules(ctx, category, json_output):
    """列出所有规则."""
    facade = ctx.obj["facade"]
    rules = facade.list_rules(category=category)

    if json_output:
        import json

        click.echo(json.dumps(rules, indent=2, ensure_ascii=False))
        return

    if not rules:
        console.print("[yellow]暂无规则[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Type")
    table.add_column("Enabled")

    for r in rules:
        table.add_row(
            r["id"],
            r["name"],
            r["category"],
            r["type"],
            "✓" if r["enabled"] else "✗",
        )

    console.print(table)


@rule.command("enable")
@click.argument("rule_id")
@click.pass_context
def enable(ctx, rule_id):
    """启用规则."""
    facade = ctx.obj["facade"]

    if facade.enable_rule(rule_id):
        console.print(f"[green]规则 {rule_id} 已启用[/green]")
    else:
        console.print(f"[red]规则 {rule_id} 不存在[/red]")


@rule.command("disable")
@click.argument("rule_id")
@click.pass_context
def disable(ctx, rule_id):
    """禁用规则."""
    facade = ctx.obj["facade"]

    if facade.disable_rule(rule_id):
        console.print(f"[green]规则 {rule_id} 已禁用[/green]")
    else:
        console.print(f"[red]规则 {rule_id} 不存在[/red]")
