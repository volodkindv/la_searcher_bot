from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_get_secrets():
    from archive_notifications import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_main():
    from archive_notifications import main

    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_move_first_posts_to_history_in_psql():
    from archive_notifications import main

    res = main.move_first_posts_to_history_in_psql(conn=MagicMock())
    pass


def test_move_notifications_to_history_in_psql():
    from archive_notifications import main

    res = main.move_notifications_to_history_in_psql(conn=MagicMock())
    pass


def test_sql_connect():
    from archive_notifications import main

    res = main.sql_connect()
    pass
