import pytest

from send_notifications import main
from tests.common import run_smoke


def test_check_and_save_event_id():
    res = run_smoke(main.check_and_save_event_id)
    pass


def test_check_for_notifs_to_send():
    res = run_smoke(main.check_for_notifs_to_send)
    pass


def test_check_for_number_of_notifs_to_send():
    res = run_smoke(main.check_for_number_of_notifs_to_send)
    pass


def test_finish_time_analytics():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.finish_time_analytics)
    pass


def test_iterate_over_notifications():
    res = run_smoke(main.iterate_over_notifications)
    pass


def test_main():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.main)
    pass


def test_send_single_message():
    res = run_smoke(main.send_single_message)
    pass
