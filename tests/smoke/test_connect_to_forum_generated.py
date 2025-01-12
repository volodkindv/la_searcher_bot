from datetime import date, datetime
from unittest.mock import MagicMock

from connect_to_forum import main


def test_get_user_attributes():
    res = main.get_user_attributes(user_id=MagicMock())
    pass


def test_get_user_data():
    res = main.get_user_data(data=MagicMock())
    pass


def test_get_user_id():
    res = main.get_user_id(u_name=MagicMock())
    pass


def test_login_into_forum():
    res = main.login_into_forum(forum_bot_password=MagicMock())
    pass


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_match_user_region_from_forum_to_bot():
    res = main.match_user_region_from_forum_to_bot(forum_region=MagicMock())
    pass


def test_prepare_message_for_async():
    res = main.prepare_message_for_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_process_sending_message_async():
    res = main.process_sending_message_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_send_message_async():
    res = main.send_message_async(context=MagicMock())
    pass


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass


def test_sql_connect_by_psycopg2():
    res = main.sql_connect_by_psycopg2()
    pass
