from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_add_tel_link():
    from compose_notifications import main

    res = main.add_tel_link(incoming_text=MagicMock(), modifier=MagicMock())
    pass


def test_age_writer():
    from compose_notifications import main

    res = main.age_writer(age=MagicMock())
    pass


def test_check_and_save_event_id():
    from compose_notifications import main

    res = main.check_and_save_event_id(
        context=MagicMock(),
        event=MagicMock(),
        conn=MagicMock(),
        new_record=MagicMock(),
        function_id=MagicMock(),
        triggered_by_func_id=MagicMock(),
    )
    pass


def test_check_if_need_compose_more():
    from compose_notifications import main

    with pytest.raises(Exception):
        res = main.check_if_need_compose_more(conn=MagicMock(), function_id=MagicMock())
    pass


def test_compose_com_msg_on_first_post_change():
    from compose_notifications import main

    res = main.compose_com_msg_on_first_post_change(record=MagicMock())
    pass


def test_compose_com_msg_on_inforg_comments():
    from compose_notifications import main

    res = main.compose_com_msg_on_inforg_comments(line=MagicMock())
    pass


def test_compose_com_msg_on_new_comments():
    from compose_notifications import main

    res = main.compose_com_msg_on_new_comments(line=MagicMock())
    pass


def test_compose_com_msg_on_new_topic():
    from compose_notifications import main

    with pytest.raises(Exception):
        res = main.compose_com_msg_on_new_topic(line=MagicMock())
    pass


def test_compose_com_msg_on_status_change():
    from compose_notifications import main

    res = main.compose_com_msg_on_status_change(line=MagicMock())
    pass


def test_compose_com_msg_on_title_change():
    from compose_notifications import main

    res = main.compose_com_msg_on_title_change(line=MagicMock())
    pass


def test_compose_individual_message_on_first_post_change():
    from compose_notifications import main

    res = main.compose_individual_message_on_first_post_change(new_record=MagicMock(), region_to_show=MagicMock())
    pass


def test_compose_individual_message_on_new_search():
    from compose_notifications import main

    res = main.compose_individual_message_on_new_search(
        new_record=MagicMock(),
        s_lat=MagicMock(),
        s_lon=MagicMock(),
        u_lat=MagicMock(),
        u_lon=MagicMock(),
        region_to_show=MagicMock(),
        num_of_sent=MagicMock(),
    )
    pass


def test_compose_new_records_from_change_log():
    from compose_notifications import main

    res = main.compose_new_records_from_change_log(conn=MagicMock())
    pass


def test_compose_users_list_from_users():
    from compose_notifications import main

    res = main.compose_users_list_from_users(conn=MagicMock(), new_record=MagicMock())
    pass


def test_define_dist_and_dir_to_search():
    from compose_notifications import main

    res = main.define_dist_and_dir_to_search(
        search_lat=MagicMock(), search_lon=MagicMock(), user_let=MagicMock(), user_lon=MagicMock()
    )
    pass


def test_define_family_name():
    from compose_notifications import main

    res = main.define_family_name(title_string=MagicMock(), predefined_fam_name=MagicMock())
    pass


def test_delete_ended_search_following():
    from compose_notifications import main

    res = main.delete_ended_search_following(conn=MagicMock(), new_record=MagicMock())
    pass


def test_enrich_new_record_from_searches():
    from compose_notifications import main

    res = main.enrich_new_record_from_searches(conn=MagicMock(), r_line=MagicMock())
    pass


def test_enrich_new_record_with_clickable_name():
    from compose_notifications import main

    res = main.enrich_new_record_with_clickable_name(line=MagicMock())
    pass


def test_enrich_new_record_with_com_message_texts():
    from compose_notifications import main

    res = main.enrich_new_record_with_com_message_texts(line=MagicMock())
    pass


def test_enrich_new_record_with_comments():
    from compose_notifications import main

    res = main.enrich_new_record_with_comments(conn=MagicMock(), type_of_comments=MagicMock(), r_line=MagicMock())
    pass


def test_enrich_new_record_with_emoji():
    from compose_notifications import main

    with pytest.raises(Exception):
        res = main.enrich_new_record_with_emoji(line=MagicMock())
    pass


def test_enrich_new_record_with_managers():
    from compose_notifications import main

    res = main.enrich_new_record_with_managers(conn=MagicMock(), r_line=MagicMock())
    pass


def test_enrich_new_record_with_search_activities():
    from compose_notifications import main

    res = main.enrich_new_record_with_search_activities(conn=MagicMock(), r_line=MagicMock())
    pass


def test_enrich_users_list_with_age_periods():
    from compose_notifications import main

    res = main.enrich_users_list_with_age_periods(conn=MagicMock(), list_of_users=MagicMock())
    pass


def test_enrich_users_list_with_radius():
    from compose_notifications import main

    res = main.enrich_users_list_with_radius(conn=MagicMock(), list_of_users=MagicMock())
    pass


def test_generate_random_function_id():
    from compose_notifications import main

    res = main.generate_random_function_id()
    pass


def test_generate_yandex_maps_place_link2():
    from compose_notifications import main

    res = main.generate_yandex_maps_place_link2(lat=MagicMock(), lon=MagicMock(), param=MagicMock())
    pass


def test_get_coords_from_list():
    from compose_notifications import main

    res = main.get_coords_from_list(input_list=MagicMock())
    pass


def test_get_list_of_admins_and_testers():
    from compose_notifications import main

    res = main.get_list_of_admins_and_testers(conn=MagicMock())
    pass


def test_get_secrets():
    from compose_notifications import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_get_triggering_function():
    from compose_notifications import main

    res = main.get_triggering_function(message_from_pubsub=MagicMock())
    pass


def test_iterate_over_all_users():
    from compose_notifications import main

    res = main.iterate_over_all_users(
        conn=MagicMock(),
        admins_list=MagicMock(),
        new_record=MagicMock(),
        list_of_users=MagicMock(),
        function_id=MagicMock(),
    )
    pass


def test_main():
    from compose_notifications import main

    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_mark_new_comments_as_processed():
    from compose_notifications import main

    res = main.mark_new_comments_as_processed(conn=MagicMock(), record=MagicMock())
    pass


def test_mark_new_record_as_processed():
    from compose_notifications import main

    res = main.mark_new_record_as_processed(conn=MagicMock(), new_record=MagicMock())
    pass


def test_process_pubsub_message():
    from compose_notifications import main

    res = main.process_pubsub_message(event=MagicMock())
    pass


def test_record_notification_statistics():
    from compose_notifications import main

    res = main.record_notification_statistics(conn=MagicMock())
    pass


def test_sql_connect():
    from compose_notifications import main

    res = main.sql_connect()
    pass