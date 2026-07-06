#!/usr/bin/env python3
"""Yandex Cloud Log Inspector — CLI tool for error investigation."""

import json
import logging
from datetime import timedelta

import click

from src.log_inspector._utils.analytics import _get_message, summarize_errors
from src.log_inspector._utils.yc_logging import YcLoggingClient

logger = logging.getLogger(__name__)


def _parse_duration(text: str) -> timedelta:
    """Parse duration string like '24h', '7d', '30m' into timedelta."""
    text = text.strip().lower()
    if text.endswith('h'):
        return timedelta(hours=int(text[:-1]))
    if text.endswith('d'):
        return timedelta(days=int(text[:-1]))
    if text.endswith('m'):
        return timedelta(minutes=int(text[:-1]))
    if text.endswith('s'):
        return timedelta(seconds=int(text[:-1]))
    raise ValueError(f'Unrecognized duration format: {text!r} (use e.g. 24h, 7d, 30m)')


@click.group()
@click.option('--folder', default=None, help='Yandex Cloud folder ID (default: YC_FOLDER_ID env var)')
@click.pass_context
def cli(ctx, folder):
    """Yandex Cloud Log Inspector — CLI tool for error investigation.

    Examples:

        \b
        # List available log groups
        python -m src.log_inspector.main list-groups

        \b
        # Find top errors in the last 24 hours
        python -m src.log_inspector.main top-errors --group <log_group_id> --since 24h

        \b
        # Trace a specific request_id
        python -m src.log_inspector.main trace --group <log_group_id> --request-id <req_id>
    """
    ctx.ensure_object(dict)
    ctx.obj['folder'] = folder
    logging.basicConfig(level=logging.WARNING)


@cli.command()
@click.pass_context
def list_groups(ctx):
    """List available log groups."""
    client = YcLoggingClient(folder_id=ctx.obj['folder'])
    try:
        groups = client.list_log_groups()
        if not groups:
            click.echo('No log groups found.')
            return

        click.echo(f'Found {len(groups)} log group(s):')
        click.echo('')
        for g in groups:
            gid = g.get('id', '?')
            name = g.get('name', '(unnamed)')
            desc = g.get('description', '')
            click.echo(f'  {gid}  — {name}')
            if desc:
                click.echo(f'           {desc}')
    finally:
        client.close()


@cli.command()
@click.option('--group', required=True, help='Log group ID')
@click.option('--since', default='24h', show_default=True, help='Lookback period (e.g. 24h, 7d, 30m)')
@click.option('--level', default='ERROR', show_default=True, help='Minimum log level')
@click.option('--top', type=int, default=10, show_default=True, help='Show top N error patterns')
@click.option('--max', 'max_entries', type=int, default=5000, show_default=True, help='Max entries to scan')
@click.pass_context
def top_errors(ctx, group, since, level, top, max_entries):
    """Find most frequent errors."""
    duration = _parse_duration(since)

    client = YcLoggingClient(folder_id=ctx.obj['folder'])
    try:
        click.echo(f'Querying {level}-level logs from last {since}...', err=True)
        entries = client.read_all_logs(
            group,
            level=level,
            since=duration,
            max_entries=max_entries,
        )
        click.echo(f'  Retrieved {len(entries)} entries.', err=True)
        click.echo(err=True)

        summary = summarize_errors(entries, top_n=top)
        click.echo(summary)
    finally:
        client.close()


@cli.command()
@click.option('--group', required=True, help='Log group ID')
@click.option('--request-id', required=True, help='Request ID to trace')
@click.option('--since', default='24h', show_default=True, help='Lookback period (e.g. 24h, 7d, 30m)')
@click.option('--max', 'max_entries', type=int, default=500, show_default=True, help='Max entries to return')
@click.pass_context
def trace(ctx, group, request_id, since, max_entries):
    """Show all logs for a specific request_id."""
    duration = _parse_duration(since)

    client = YcLoggingClient(folder_id=ctx.obj['folder'])
    try:
        entries = client.get_logs_by_request_id(
            group,
            request_id,
            since=duration,
            max_entries=max_entries,
        )

        if not entries:
            click.echo(f'No log entries found for request_id={request_id}')
            return

        click.echo(f'Found {len(entries)} log entries for request_id={request_id}:')
        click.echo('')

        for entry in sorted(entries, key=lambda e: e.get('timestamp', '')):
            ts = entry.get('timestamp', '?')
            level = entry.get('level', entry.get('severity', '?')).ljust(7)
            msg = _get_message(entry)
            click.echo(f'  [{ts}] {level} {msg[:300]}')
    finally:
        client.close()


@cli.command()
@click.option('--group', required=True, help='Log group ID')
@click.option('--since', default='24h', show_default=True, help='Lookback period (e.g. 24h, 7d, 30m)')
@click.option('--level', default='ERROR', show_default=True, help='Minimum log level')
@click.option('--filter', 'filter_str', default=None, help='Additional filter string')
@click.option('--max', 'max_entries', type=int, default=100, show_default=True, help='Max entries to return')
@click.pass_context
def raw(ctx, group, since, level, filter_str, max_entries):
    """Dump raw JSON logs for programmatic use."""
    duration = _parse_duration(since)

    client = YcLoggingClient(folder_id=ctx.obj['folder'])
    try:
        entries = client.read_all_logs(
            group,
            level=level,
            since=duration,
            filter_str=filter_str,
            max_entries=max_entries,
        )
        click.echo(json.dumps(entries, indent=2, ensure_ascii=False, default=str))
    finally:
        client.close()


if __name__ == '__main__':
    cli()
