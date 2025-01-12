from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_get_secrets():
    from manage_users import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_main():
    from manage_users import main

    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_process_pubsub_message():
    from manage_users import main

    res = main.process_pubsub_message(event=MagicMock())
    pass


def test_save_default_notif_settings():
    from manage_users import main

    with pytest.raises(Exception):
        res = main.save_default_notif_settings(user_id=MagicMock())
    pass


def test_save_new_user():
    from manage_users import main

    with pytest.raises(Exception):
        res = main.save_new_user(user_id=MagicMock(), username=MagicMock(), timestamp=MagicMock())
    pass


def test_save_onboarding_step():
    from manage_users import main

    with pytest.raises(Exception):
        res = main.save_onboarding_step(user_id=MagicMock(), step_name=MagicMock(), timestamp=MagicMock())
    pass


def test_save_updated_status_for_user():
    from manage_users import main

    with pytest.raises(Exception):
        res = main.save_updated_status_for_user(action=MagicMock(), user_id=MagicMock(), timestamp=MagicMock())
    pass


def test_sql_connect_by_psycopg2():
    from manage_users import main

    res = main.sql_connect_by_psycopg2()
    pass
