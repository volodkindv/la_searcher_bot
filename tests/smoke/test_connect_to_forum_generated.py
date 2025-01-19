import pytest

from connect_to_forum import main
from tests.common import run_smoke


def test_get_user_attributes():
    res = run_smoke(main.get_user_attributes)
    pass


def test_get_user_data():
    res = run_smoke(main.get_user_data)
    pass


def test_get_user_id():
    res = run_smoke(main.get_user_id)
    pass


def test_login_into_forum():
    res = run_smoke(main.login_into_forum)
    pass


def test_main():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.main)
    pass


def test_match_user_region_from_forum_to_bot():
    res = run_smoke(main.match_user_region_from_forum_to_bot)
    pass


def test_prepare_message_for_async():
    res = run_smoke(main.prepare_message_for_async)
    pass


def test_process_sending_message_async():
    res = run_smoke(main.process_sending_message_async)
    pass


def test_send_message_async():
    res = run_smoke(main.send_message_async)
    pass


def test_sql_connect_by_psycopg2_with_globals():
    res = run_smoke(main.sql_connect_by_psycopg2_with_globals)
    pass
