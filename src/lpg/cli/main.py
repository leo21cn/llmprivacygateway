"""CLI main entry point."""

import click
from lpg.core.service_facade import ServiceFacade
from lpg.cli.commands import start, stop, status, config, key, rule, provider, log


@click.group()
@click.version_option(version="1.0.0")
@click.option("-c", "--config", "config_path", help="配置文件路径")
@click.option("-v", "--verbose", is_flag=True, help="详细输出模式")
@click.option("-q", "--quiet", is_flag=True, help="静默模式")
@click.option("-j", "--json", "json_output", is_flag=True, help="JSON 格式输出")
@click.pass_context
def cli(ctx, config_path, verbose, quiet, json_output):
    """LLM Privacy Gateway - 本地隐私保护代理."""
    ctx.ensure_object(dict)
    ctx.obj["facade"] = ServiceFacade(config_path)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    ctx.obj["json_output"] = json_output


cli.add_command(start.start)
cli.add_command(stop.stop)
cli.add_command(status.status)
cli.add_command(config.config)
cli.add_command(key.key)
cli.add_command(rule.rule)
cli.add_command(provider.provider)
cli.add_command(log.log)
