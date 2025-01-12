from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_generate_random_function_id():
    from manage_topics import main

    res = main.generate_random_function_id()
    pass


def test_get_secrets():
    from manage_topics import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_main():
    from manage_topics import main

    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_process_pubsub_message():
    from manage_topics import main

    with pytest.raises(Exception):
        res = main.process_pubsub_message(event=MagicMock())
    pass


def test_save_function_into_register():
    from manage_topics import main

    res = main.save_function_into_register(
        context=MagicMock(), start_time=MagicMock(), function_id=MagicMock(), change_log_id=MagicMock()
    )
    pass


def test_save_status_for_topic():
    from manage_topics import main

    res = main.save_status_for_topic(topic_id=MagicMock(), status=MagicMock())
    pass


def test_save_visibility_for_topic():
    from manage_topics import main

    res = main.save_visibility_for_topic(topic_id=MagicMock(), visibility=MagicMock())
    pass


def test_sql_connect():
    from manage_topics import main

    res = main.sql_connect()
    pass
