from unittest.mock import MagicMock

from archive_notifications import main


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_move_first_posts_to_history_in_psql():
    res = main.move_first_posts_to_history_in_psql(conn=MagicMock())
    pass


def test_move_notifications_to_history_in_psql():
    res = main.move_notifications_to_history_in_psql(conn=MagicMock())
    pass


def test_publish_to_pubsub():
    res = main.publish_to_pubsub(topic_name=MagicMock(), message=MagicMock())
    pass


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass


def test_sql_connect():
    res = main.sql_connect()
    pass
