from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_get_secrets():
    from users_activate import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_main():
    from users_activate import main

    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_mark_up_onboarding_status_0():
    from users_activate import main

    res = main.mark_up_onboarding_status_0(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_0_2():
    from users_activate import main

    res = main.mark_up_onboarding_status_0_2(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_10():
    from users_activate import main

    res = main.mark_up_onboarding_status_10(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_10_2():
    from users_activate import main

    res = main.mark_up_onboarding_status_10_2(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_20():
    from users_activate import main

    res = main.mark_up_onboarding_status_20(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_21():
    from users_activate import main

    res = main.mark_up_onboarding_status_21(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80():
    from users_activate import main

    res = main.mark_up_onboarding_status_80(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_have_all_settings():
    from users_activate import main

    res = main.mark_up_onboarding_status_80_have_all_settings(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_just_got_summaries():
    from users_activate import main

    res = main.mark_up_onboarding_status_80_just_got_summaries(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_patch():
    from users_activate import main

    res = main.mark_up_onboarding_status_80_patch(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_self_deactivated():
    from users_activate import main

    res = main.mark_up_onboarding_status_80_self_deactivated(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_wo_dialogs():
    from users_activate import main

    res = main.mark_up_onboarding_status_80_wo_dialogs(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_99():
    from users_activate import main

    res = main.mark_up_onboarding_status_99(cur=MagicMock())
    pass


def test_process_pubsub_message():
    from users_activate import main

    res = main.process_pubsub_message(event=MagicMock())
    pass


def test_sql_connect_by_psycopg2():
    from users_activate import main

    res = main.sql_connect_by_psycopg2()
    pass
