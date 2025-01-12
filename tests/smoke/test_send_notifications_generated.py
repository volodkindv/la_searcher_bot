from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from send_notifications import main


def test_check_and_save_event_id():
    res = main.check_and_save_event_id(
        context=MagicMock(),
        event=MagicMock(),
        function_id=MagicMock(),
        changed_ids=MagicMock(),
        triggered_by_func_id=MagicMock(),
    )
    pass


def test_check_for_notifs_to_send():
    res = main.check_for_notifs_to_send(cur=MagicMock())
    pass


def test_check_for_number_of_notifs_to_send():
    res = main.check_for_number_of_notifs_to_send(cur=MagicMock())
    pass


def test_finish_time_analytics():
    with pytest.raises(Exception):
        res = main.finish_time_analytics(
            notif_times=MagicMock(), delays=MagicMock(), parsed_times=MagicMock(), list_of_change_ids=MagicMock()
        )
    pass


def test_generate_random_function_id():
    res = main.generate_random_function_id()
    pass


def test_get_change_log_update_time():
    res = main.get_change_log_update_time(cur=MagicMock(), change_log_id=MagicMock())
    pass


def test_get_triggering_function():
    res = main.get_triggering_function(message_from_pubsub=MagicMock())
    pass


def test_iterate_over_notifications():
    with pytest.raises(Exception):
        res = main.iterate_over_notifications(
            bot_token=MagicMock(),
            admin_id=MagicMock(),
            script_start_time=MagicMock(),
            session=MagicMock(),
            function_id=MagicMock(),
        )
    pass


def test_main():
    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_process_pubsub_message():
    res = main.process_pubsub_message(event={})
    pass


def test_process_response():
    res = main.process_response(user_id=MagicMock(), response=MagicMock())
    pass


def test_save_sending_status_to_notif_by_user():
    res = main.save_sending_status_to_notif_by_user(cur=MagicMock(), message_id=MagicMock(), result=MagicMock())
    pass


def test_send_location_to_api():
    res = main.send_location_to_api(session=MagicMock(), bot_token=MagicMock(), user_id=MagicMock(), params=MagicMock())
    pass


def test_send_message_to_api():
    res = main.send_message_to_api(
        session=MagicMock(), bot_token=MagicMock(), user_id=MagicMock(), message=MagicMock(), params=MagicMock()
    )
    pass


def test_send_single_message():
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
    res = main.sql_connect_by_psycopg2()
    pass
