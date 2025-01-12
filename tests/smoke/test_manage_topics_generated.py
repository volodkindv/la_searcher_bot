from unittest.mock import MagicMock

from manage_topics import main


def test_generate_random_function_id():
    res = main.generate_random_function_id()
    pass


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_notify_admin():
    res = main.notify_admin(message=MagicMock())
    pass


def test_process_pubsub_message():
    res = main.process_pubsub_message(event=MagicMock())
    pass


def test_publish_to_pubsub():
    res = main.publish_to_pubsub(topic_name=MagicMock(), message=MagicMock())
    pass


def test_save_function_into_register():
    res = main.save_function_into_register(
        context=MagicMock(), start_time=MagicMock(), function_id=MagicMock(), change_log_id=MagicMock()
    )
    pass


def test_save_status_for_topic():
    res = main.save_status_for_topic(topic_id=MagicMock(), status=MagicMock())
    pass


def test_save_visibility_for_topic():
    res = main.save_visibility_for_topic(topic_id=MagicMock(), visibility=MagicMock())
    pass


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass


def test_sql_connect():
    res = main.sql_connect()
    pass
