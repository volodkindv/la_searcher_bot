from unittest.mock import MagicMock

from users_activate import main


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_mark_up_onboarding_status_0():
    res = main.mark_up_onboarding_status_0(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_0_2():
    res = main.mark_up_onboarding_status_0_2(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_10():
    res = main.mark_up_onboarding_status_10(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_10_2():
    res = main.mark_up_onboarding_status_10_2(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_20():
    res = main.mark_up_onboarding_status_20(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_21():
    res = main.mark_up_onboarding_status_21(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80():
    res = main.mark_up_onboarding_status_80(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_have_all_settings():
    res = main.mark_up_onboarding_status_80_have_all_settings(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_just_got_summaries():
    res = main.mark_up_onboarding_status_80_just_got_summaries(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_patch():
    res = main.mark_up_onboarding_status_80_patch(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_self_deactivated():
    res = main.mark_up_onboarding_status_80_self_deactivated(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_80_wo_dialogs():
    res = main.mark_up_onboarding_status_80_wo_dialogs(cur=MagicMock())
    pass


def test_mark_up_onboarding_status_99():
    res = main.mark_up_onboarding_status_99(cur=MagicMock())
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


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass


def test_sql_connect_by_psycopg2():
    res = main.sql_connect_by_psycopg2()
    pass
