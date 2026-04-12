"""Key command."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def key():
    """虚拟 Key 管理."""
    pass


@key.command("list")
@click.option("-j", "--json", "json_output", is_flag=True, help="JSON 格式输出")
@click.pass_context
def list_keys(ctx, json_output):
    """列出所有虚拟 Key."""
    facade = ctx.obj["facade"]
    keys = facade.list_virtual_keys()

    if json_output:
        import json

        click.echo(json.dumps(keys, indent=2, ensure_ascii=False))
        return

    if not keys:
        console.print("[yellow]暂无虚拟 Key[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Provider")
    table.add_column("Usage")

    for k in keys:
        table.add_row(k["id"], k["name"], k["provider"], str(k.get("usage_count", 0)))

    console.print(table)


@key.command("create")
@click.option("-p", "--provider", required=True, help="关联的提供商名称")
@click.option("-n", "--name", required=True, help="Key 标识名称")
@click.option("-e", "--expire", help="过期时间")
@click.pass_context
def create(ctx, provider, name, expire):
    """创建新的虚拟 Key."""
    facade = ctx.obj["facade"]

    try:
        result = facade.create_virtual_key(
            provider=provider, name=name, expires_at=expire
        )
        console.print(f"[green]虚拟 Key 创建成功[/green]")
        console.print(f"Key ID: {result['id']}")
        console.print(f"Virtual Key: {result['virtual_key']}")
    except ValueError as e:
        console.print(f"[red]错误: {e}[/red]")
        raise SystemExit(1)


@key.command("revoke")
@click.argument("key_id")
@click.pass_context
def revoke(ctx, key_id):
    """吊销虚拟 Key."""
    facade = ctx.obj["facade"]

    if facade.revoke_virtual_key(key_id):
        console.print(f"[green]Key {key_id} 已吊销[/green]")
    else:
        console.print(f"[red]Key {key_id} 不存在[/red]")
