from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_get_secrets():
    from connect_to_forum import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_get_user_attributes():
    from connect_to_forum import main

    with pytest.raises(Exception):
        res = main.get_user_attributes(user_id=MagicMock())
    pass


def test_get_user_data():
    from connect_to_forum import main

    res = main.get_user_data(data=MagicMock())
    pass


def test_get_user_id():
    from connect_to_forum import main

    with pytest.raises(Exception):
        res = main.get_user_id(u_name=MagicMock())
    pass


def test_login_into_forum():
    from connect_to_forum import main

    with pytest.raises(Exception):
        res = main.login_into_forum(forum_bot_password=MagicMock())
    pass


def test_main():
    from connect_to_forum import main

    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_match_user_region_from_forum_to_bot():
    from connect_to_forum import main

    res = main.match_user_region_from_forum_to_bot(forum_region=MagicMock())
    pass


def test_prepare_message_for_async():
    from connect_to_forum import main

    res = main.prepare_message_for_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_process_sending_message_async():
    from connect_to_forum import main

    with pytest.raises(Exception):
        res = main.process_sending_message_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_send_message_async():
    from connect_to_forum import main

    res = main.send_message_async(context=MagicMock())
    pass


def test_sql_connect_by_psycopg2():
    from connect_to_forum import main

    res = main.sql_connect_by_psycopg2()
    pass
