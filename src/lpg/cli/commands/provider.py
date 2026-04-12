"""Provider command."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def provider():
    """LLM 提供商管理."""
    pass


@provider.command("list")
@click.option("-j", "--json", "json_output", is_flag=True, help="JSON 格式输出")
@click.pass_context
def list_providers(ctx, json_output):
    """列出已配置的提供商."""
    facade = ctx.obj["facade"]
    providers = facade.list_providers()

    if json_output:
        import json

        click.echo(json.dumps(providers, indent=2, ensure_ascii=False))
        return

    if not providers:
        console.print("[yellow]暂无提供商配置[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Base URL")

    for p in providers:
        table.add_row(p["name"], p["type"], p["base_url"])

    console.print(table)


@provider.command("add")
@click.option("-t", "--type", "provider_type", required=True, help="提供商类型")
@click.option("-n", "--name", required=True, help="提供商名称")
@click.option("-u", "--base-url", required=True, help="API 基础 URL")
@click.option("-k", "--api-key-file", help="API Key 文件路径")
@click.pass_context
def add(ctx, provider_type, name, base_url, api_key_file):
    """添加新提供商."""
    facade = ctx.obj["facade"]

    result = facade.add_provider(
        provider_type=provider_type,
        name=name,
        base_url=base_url,
        api_key_file=api_key_file,
    )
    console.print(f"[green]提供商 {name} 已添加[/green]")
