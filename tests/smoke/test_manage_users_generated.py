from datetime import date, datetime
from unittest.mock import MagicMock

from manage_users import main


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_process_pubsub_message():
    res = main.process_pubsub_message(event={})
    pass


def test_save_default_notif_settings():
    res = main.save_default_notif_settings(user_id=MagicMock())
    pass


def test_save_new_user():
    res = main.save_new_user(user_id=1, username='foo', timestamp=MagicMock())
    pass


def test_save_onboarding_step():
    res = main.save_onboarding_step(user_id=MagicMock(), step_name=MagicMock(), timestamp=MagicMock())
    pass


def test_save_updated_status_for_user():
    res = main.save_updated_status_for_user(action=MagicMock(), user_id=MagicMock(), timestamp=MagicMock())
    pass


def test_sql_connect_by_psycopg2():
    res = main.sql_connect_by_psycopg2()
    pass
