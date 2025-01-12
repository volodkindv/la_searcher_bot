from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_check_and_save_event_id():
    from send_notifications_helper import main

    res = main.check_and_save_event_id(
        context=MagicMock(),
        event=MagicMock(),
        function_id=MagicMock(),
        changed_ids=MagicMock(),
        triggered_by_func_id=MagicMock(),
    )
    pass


def test_check_first_notif_to_send():
    from send_notifications_helper import main

    res = main.check_first_notif_to_send(cur=MagicMock())
    pass


def test_check_for_notifs_to_send():
    from send_notifications_helper import main

    res = main.check_for_notifs_to_send(cur=MagicMock(), first_message=MagicMock())
    pass


def test_finish_time_analytics():
    from send_notifications_helper import main

    with pytest.raises(Exception):
        res = main.finish_time_analytics(
            notif_times=MagicMock(), delays=MagicMock(), parsed_times=MagicMock(), list_of_change_ids=MagicMock()
        )
    pass


def test_generate_random_function_id():
    from send_notifications_helper import main

    res = main.generate_random_function_id()
    pass


def test_get_change_log_update_time():
    from send_notifications_helper import main

    res = main.get_change_log_update_time(cur=MagicMock(), change_log_id=MagicMock())
    pass


def test_get_secrets():
    from send_notifications_helper import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_get_triggering_function():
    from send_notifications_helper import main

    res = main.get_triggering_function(message_from_pubsub=MagicMock())
    pass


def test_iterate_over_notifications():
    from send_notifications_helper import main

    res = main.iterate_over_notifications(
        bot_token=MagicMock(),
        admin_id=MagicMock(),
        script_start_time=MagicMock(),
        session=MagicMock(),
        function_id=MagicMock(),
    )
    pass


def test_main():
    from send_notifications_helper import main

    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_process_pubsub_message():
    from send_notifications_helper import main

    res = main.process_pubsub_message(event=MagicMock())
    pass


def test_process_response():
    from send_notifications_helper import main

    res = main.process_response(user_id=MagicMock(), response=MagicMock())
    pass


def test_save_sending_status_to_notif_by_user():
    from send_notifications_helper import main

    res = main.save_sending_status_to_notif_by_user(cur=MagicMock(), message_id=MagicMock(), result=MagicMock())
    pass


def test_send_location_to_api():
    from send_notifications_helper import main

    res = main.send_location_to_api(session=MagicMock(), bot_token=MagicMock(), user_id=MagicMock(), params=MagicMock())
    pass


def test_send_message_to_api():
    from send_notifications_helper import main

    res = main.send_message_to_api(
        session=MagicMock(), bot_token=MagicMock(), user_id=MagicMock(), message=MagicMock(), params=MagicMock()
    )
    pass


def test_send_single_message():
    from send_notifications_helper import main

    res = main.send_single_message(
        bot_token=MagicMock(),
        user_id=MagicMock(),
        message_content=MagicMock(),
        message_params=MagicMock(),
        message_type=MagicMock(),
        admin_id=MagicMock(),
        session=MagicMock(),
    )
    pass


def test_sql_connect_by_psycopg2():
    from send_notifications_helper import main

    res = main.sql_connect_by_psycopg2()
    pass
