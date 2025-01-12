from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_archive_notif_by_user():
    from archive_to_bigquery import main

    res = main.archive_notif_by_user(client=MagicMock())
    pass


def test_get_secrets():
    from archive_to_bigquery import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_main():
    from archive_to_bigquery import main

    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_save_sql_stat_table_sizes():
    from archive_to_bigquery import main

    res = main.save_sql_stat_table_sizes(client=MagicMock())
    pass


def test_sql_connect():
    from archive_to_bigquery import main

    res = main.sql_connect()
    pass
