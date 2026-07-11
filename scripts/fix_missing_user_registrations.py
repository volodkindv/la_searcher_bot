"""Find and fix users who have settings but no record in the ``users`` table.

Background
----------
Commit ``608fa17e`` (PR #907) added centralised user registration in the MAX
and VK bots. Before that fix, a user who sent any message *other* than
``/start`` or ``bot_started`` (e.g., a location pin, arbitrary text, or an
inline callback) would have their settings saved (radius, coordinates,
regional preferences, topic types, etc.) **without** a corresponding record
in the ``users`` table.

This script:
1. Finds all ``user_id`` values that exist in any settings table but are
   missing from ``users``.
2. For each such user, creates a minimal record in ``users``,
   ``user_identity_map``, ``user_onboarding``, ``user_preferences``, and
   ``user_pref_topic_type`` (default topic types).

Usage
-----
Dry-run (safe — only prints what would be done)::

    PYTHONPATH=src uv run python scripts/fix_missing_user_registrations.py --dry-run

Apply fixes::

    PYTHONPATH=src uv run python scripts/fix_missing_user_registrations.py

Run with a custom DSN (default: from ``AppConfig`` env vars)::

    PYTHONPATH=src uv run python scripts/fix_missing_user_registrations.py --dsn=postgresql://user:pass@host:5432/db
"""

from __future__ import annotations

import datetime
import logging
import sys
from typing import Any

import click
import sqlalchemy

from _dependencies.common.commons import Messenger, sqlalchemy_get_pool

logger = logging.getLogger(__name__)

# ─── Tables that store user_id but have NO FK constraint to users ───────
# These are the "settings" tables where orphan user_ids can exist.
# NOTE: user_identity_map uses internal_user_id, not user_id — handled separately.
SETTINGS_TABLES = [
    'user_coordinates',
    'user_pref_radius',
    'user_regional_preferences',
    'user_preferences',
    'user_pref_age',
    'user_pref_topic_type',
    'user_pref_urgency',
    'user_pref_search_filtering',
    'user_pref_search_whitelist',
    'user_onboarding',
    'user_forum_attributes',
    'user_roles',
    'user_stat',
    'dialogs',
    'communications_last_inline_msg',
    'notif_by_user',
]


def find_orphan_user_ids(conn: Any) -> set[int]:
    """Return all ``user_id`` values that exist in settings tables but NOT in ``users``."""
    all_user_ids: set[int] = set()
    users_ids: set[int] = set()

    for table in SETTINGS_TABLES:
        try:
            rows = conn.execute(
                sqlalchemy.text(f'SELECT DISTINCT user_id FROM {table} WHERE user_id IS NOT NULL')
            ).fetchall()
            all_user_ids.update(row[0] for row in rows)
        except Exception as exc:
            logger.warning('Could not read table %s: %s', table, exc)

    # Also check user_identity_map (uses internal_user_id, not user_id)
    try:
        rows = conn.execute(
            sqlalchemy.text(
                'SELECT DISTINCT internal_user_id FROM user_identity_map WHERE internal_user_id IS NOT NULL'
            )
        ).fetchall()
        all_user_ids.update(row[0] for row in rows)
    except Exception as exc:
        logger.warning('Could not read table user_identity_map: %s', exc)

    try:
        rows = conn.execute(sqlalchemy.text('SELECT user_id FROM users WHERE user_id IS NOT NULL')).fetchall()
        users_ids.update(row[0] for row in rows)
    except Exception as exc:
        logger.error('Could not read users table: %s', exc)
        sys.exit(1)

    orphans = all_user_ids - users_ids
    return orphans


def _guess_messenger(conn: Any, user_id: int) -> Messenger:
    """Try to guess the messenger for an orphan user based on available data.

    Heuristic:
    1. If ``user_identity_map`` has a record for this user_id, use its messenger.
    2. If ``dialogs`` has a record, assume Telegram (most common).
    3. Default to Telegram.
    """
    try:
        row = conn.execute(
            sqlalchemy.text(
                'SELECT messenger FROM user_identity_map WHERE internal_user_id=:uid LIMIT 1'
            ),
            {'uid': user_id},
        ).fetchone()
        if row:
            return Messenger(row[0])
    except Exception:
        pass

    return Messenger.TELEGRAM


def _guess_username(conn: Any, user_id: int) -> str | None:
    """Try to find a display name for the user from dialogs."""
    try:
        row = conn.execute(
            sqlalchemy.text(
                """SELECT message_text FROM dialogs
                   WHERE user_id=:uid AND message_text IS NOT NULL
                   ORDER BY id ASC LIMIT 1"""
            ),
            {'uid': user_id},
        ).fetchone()
        if row:
            text = row[0].strip()
            if text and not text.startswith('/'):
                return text[:100]
    except Exception:
        pass
    return None


def register_orphan_user(
    conn: Any,
    user_id: int,
    messenger: Messenger,
    username: str | None,
    now: datetime.datetime,
) -> None:
    """Create a minimal user record for an orphan user_id.

    This mirrors ``register_new_user()`` + ``register_vk_only_user()`` but
    without the ``ON CONFLICT DO NOTHING`` guard — we already know the user
    doesn't exist.
    """
    # 1. Insert into users
    conn.execute(
        sqlalchemy.text("""
            INSERT INTO users (user_id, internal_user_id, username_telegram, reg_date, status)
            VALUES (:user_id, :internal_user_id, :username, :reg_date, :status)
        """),
        {
            'user_id': user_id,
            'internal_user_id': user_id,
            'username': username,
            'reg_date': now,
            'status': 'new',
        },
    )

    # 2. Insert into user_identity_map (if not already there)
    conn.execute(
        sqlalchemy.text("""
            INSERT INTO user_identity_map (internal_user_id, messenger, messenger_user_id)
            VALUES (:internal_user_id, :messenger, :messenger_user_id)
            ON CONFLICT (messenger, messenger_user_id) DO NOTHING
        """),
        {
            'internal_user_id': user_id,
            'messenger': messenger.value,
            'messenger_user_id': str(user_id),
        },
    )

    # 3. Insert onboarding start
    conn.execute(
        sqlalchemy.text("""
            INSERT INTO user_onboarding (user_id, step_id, step_name, timestamp)
            VALUES (:user_id, :step_id, :step_name, :timestamp)
            ON CONFLICT DO NOTHING
        """),
        {'user_id': user_id, 'step_id': 0, 'step_name': 'start', 'timestamp': now},
    )

    # 4. Insert default notification preferences (if not already there)
    default_prefs = [
        (user_id, 'new_searches', 0),
        (user_id, 'status_changes', 1),
        (user_id, 'inforg_comments', 4),
        (user_id, 'first_post_changes', 8),
        (user_id, 'bot_news', 20),
    ]
    for uid, pref, pref_id in default_prefs:
        conn.execute(
            sqlalchemy.text("""
                INSERT INTO user_preferences (user_id, preference, pref_id)
                VALUES (:user_id, :preference, :pref_id)
                ON CONFLICT (user_id, pref_id) DO NOTHING
            """),
            {'user_id': uid, 'preference': pref, 'pref_id': pref_id},
        )

    # 5. Insert default topic types (if not already there)
    default_topic_types = [
        (user_id, 0, 'search_works'),
        (user_id, 1, 'info_search'),
    ]
    for uid, type_id, type_name in default_topic_types:
        conn.execute(
            sqlalchemy.text("""
                INSERT INTO user_pref_topic_type (user_id, topic_type_id, topic_type_name, timestamp)
                VALUES (:user_id, :topic_type_id, :topic_type_name, :timestamp)
                ON CONFLICT (user_id, topic_type_id) DO NOTHING
            """),
            {'user_id': uid, 'topic_type_id': type_id, 'topic_type_name': type_name, 'timestamp': now},
        )

    # 6. Insert user_statuses_history
    conn.execute(
        sqlalchemy.text("""
            INSERT INTO user_statuses_history (status, date, user_id)
            VALUES (:status, :date, :user_id)
            ON CONFLICT (user_id, date) DO NOTHING
        """),
        {'status': 'new', 'date': now, 'user_id': user_id},
    )


@click.command()
@click.option('--dry-run', is_flag=True, help='Only print what would be done, do not modify the database.')
@click.option('--dsn', default=None, help='PostgreSQL DSN (default: from AppConfig environment variables).')
def main(dry_run: bool, dsn: str | None) -> None:
    """Find and fix users who have settings but no record in the users table."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    if dsn:
        engine = sqlalchemy.create_engine(dsn)
        with engine.begin() as conn:
            _run(conn, dry_run)
    else:
        pool = sqlalchemy_get_pool()
        with pool.begin() as conn:
            _run(conn, dry_run)


def _run(conn: Any, dry_run: bool) -> None:
    """Core logic: find orphans and optionally register them."""
    now = datetime.datetime.now()

    orphans = find_orphan_user_ids(conn)

    if not orphans:
        logger.info('No orphan user_ids found. All users have records in the users table.')
        return

    logger.info('Found %d orphan user_id(s) with settings but no users record:', len(orphans))

    for uid in sorted(orphans):
        tables_found = []
        for table in SETTINGS_TABLES:
            try:
                row = conn.execute(
                    sqlalchemy.text(f'SELECT 1 FROM {table} WHERE user_id=:uid LIMIT 1'),
                    {'uid': uid},
                ).fetchone()
                if row:
                    tables_found.append(table)
            except Exception:
                pass

        messenger = _guess_messenger(conn, uid)
        username = _guess_username(conn, uid)

        logger.info(
            '  user_id=%-8s  messenger=%-10s  username=%-20s  tables=%s',
            uid,
            messenger.value,
            username or '(none)',
            ', '.join(tables_found),
        )

        if not dry_run:
            register_orphan_user(conn, uid, messenger, username, now)
            logger.info('    → Registered user_id=%s', uid)

    if dry_run:
        logger.info('Dry-run complete. Use --dry-run to preview, omit to apply.')
    else:
        logger.info('Done. Registered %d user(s).', len(orphans))


if __name__ == '__main__':
    main()
