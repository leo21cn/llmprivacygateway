"""Config command."""

import click
from rich.console import Console

console = Console()


@click.group()
def config():
    """配置管理."""
    pass


@config.command()
@click.pass_context
def init(ctx):
    """初始化配置文件."""
    facade = ctx.obj["facade"]
    facade.init_config()
    console.print("[green]配置文件已初始化[/green]")


@config.command()
@click.pass_context
def show(ctx):
    """显示当前配置."""
    facade = ctx.obj["facade"]
    config_data = facade.get_config()
    import json

    # Handle Pydantic model or dict
    if hasattr(config_data, "model_dump"):
        config_dict = config_data.model_dump()
    elif hasattr(config_data, "__dict__"):
        config_dict = config_data.__dict__
    else:
        config_dict = config_data

    click.echo(json.dumps(config_dict, indent=2, ensure_ascii=False, default=str))


@config.command()
@click.argument("key")
@click.argument("value")
@click.pass_context
def set(ctx, key, value):
    """设置配置项."""
    facade = ctx.obj["facade"]
    facade.set_config(key, value)
    console.print(f"[green]配置已更新: {key} = {value}[/green]")


@config.command()
@click.argument("key")
@click.pass_context
def get(ctx, key):
    """获取配置项."""
    facade = ctx.obj["facade"]
    value = facade.get_config(key)
    click.echo(value)
