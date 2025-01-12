from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from archive_to_bigquery import main


def test_archive_notif_by_user():
    res = main.archive_notif_by_user(client=MagicMock())
    pass


def test_main():
    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_save_sql_stat_table_sizes():
    res = main.save_sql_stat_table_sizes(client=MagicMock())
    pass


def test_sql_connect():
    res = main.sql_connect()
    pass
