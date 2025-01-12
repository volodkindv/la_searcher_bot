from unittest.mock import MagicMock

from send_debug_to_admin import main


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_prepare_message_for_async():
    res = main.prepare_message_for_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_process_pubsub_message():
    res = main.process_pubsub_message(event={})
    pass


def test_process_sending_message_async():
    res = main.process_sending_message_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_send_message():
    res = main.send_message(admin_user_id=MagicMock(), message=MagicMock())
    pass


def test_send_message_async():
    res = main.send_message_async(context=MagicMock())
    pass


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass
