from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_get_secrets():
    from send_debug_to_admin import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_main():
    from send_debug_to_admin import main

    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_prepare_message_for_async():
    from send_debug_to_admin import main

    res = main.prepare_message_for_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_process_pubsub_message():
    from send_debug_to_admin import main

    res = main.process_pubsub_message(event=MagicMock())
    pass


def test_process_sending_message_async():
    from send_debug_to_admin import main

    with pytest.raises(Exception):
        res = main.process_sending_message_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_send_message():
    from send_debug_to_admin import main

    res = main.send_message(admin_user_id=MagicMock(), message=MagicMock())
    pass


def test_send_message_async():
    from send_debug_to_admin import main

    res = main.send_message_async(context=MagicMock())
    pass
