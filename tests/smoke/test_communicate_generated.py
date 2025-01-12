from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_add_user_sys_role():
    from communicate import main

    res = main.add_user_sys_role(cur=MagicMock(), user_id=MagicMock(), sys_role_name=MagicMock())
    pass


def test_age_writer():
    from communicate import main

    res = main.age_writer(age=MagicMock())
    pass


def test_api_callback_edit_inline_keyboard():
    from communicate import main

    with pytest.raises(Exception):
        res = main.api_callback_edit_inline_keyboard(
            bot_token=MagicMock(), callback_query=MagicMock(), reply_markup=MagicMock(), user_id=MagicMock()
        )
    pass


def test_check_if_new_user():
    from communicate import main

    res = main.check_if_new_user(cur=MagicMock(), user_id=MagicMock())
    pass


def test_check_if_user_has_no_regions():
    from communicate import main

    res = main.check_if_user_has_no_regions(cur=MagicMock(), user_id=MagicMock())
    pass


def test_check_onboarding_step():
    from communicate import main

    res = main.check_onboarding_step(cur=MagicMock(), user_id=MagicMock(), user_is_new=MagicMock())
    pass


def test_compose_full_message_on_list_of_searches():
    from communicate import main

    res = main.compose_full_message_on_list_of_searches(
        cur=MagicMock(), list_type=MagicMock(), user_id=MagicMock(), region=MagicMock(), region_name=MagicMock()
    )
    pass


def test_compose_full_message_on_list_of_searches_ikb():
    from communicate import main

    res = main.compose_full_message_on_list_of_searches_ikb(
        cur=MagicMock(), list_type=MagicMock(), user_id=MagicMock(), region=MagicMock(), region_name=MagicMock()
    )
    pass


def test_compose_msg_on_active_searches_in_one_reg():
    from communicate import main

    res = main.compose_msg_on_active_searches_in_one_reg(cur=MagicMock(), region=MagicMock(), user_data=MagicMock())
    pass


def test_compose_msg_on_active_searches_in_one_reg_ikb():
    from communicate import main

    res = main.compose_msg_on_active_searches_in_one_reg_ikb(
        cur=MagicMock(), region=MagicMock(), user_data=MagicMock(), user_id=MagicMock()
    )
    pass


def test_compose_msg_on_all_last_searches():
    from communicate import main

    res = main.compose_msg_on_all_last_searches(cur=MagicMock(), region=MagicMock())
    pass


def test_compose_msg_on_all_last_searches_ikb():
    from communicate import main

    res = main.compose_msg_on_all_last_searches_ikb(cur=MagicMock(), region=MagicMock(), user_id=MagicMock())
    pass


def test_compose_msg_on_user_setting_fullness():
    from communicate import main

    res = main.compose_msg_on_user_setting_fullness(cur=MagicMock(), user_id=1)
    pass


def test_compose_user_preferences_message():
    from communicate import main

    res = main.compose_user_preferences_message(cur=MagicMock(), user_id=MagicMock())
    pass


def test_delete_last_user_inline_dialogue():
    from communicate import main

    res = main.delete_last_user_inline_dialogue(cur=MagicMock(), user_id=1)
    pass


def test_delete_user_coordinates():
    from communicate import main

    res = main.delete_user_coordinates(cur=MagicMock(), user_id=MagicMock())
    pass


def test_delete_user_sys_role():
    from communicate import main

    res = main.delete_user_sys_role(cur=MagicMock(), user_id=MagicMock(), sys_role_name=MagicMock())
    pass


def test_distance_to_search():
    from communicate import main

    res = main.distance_to_search(
        search_lat=MagicMock(),
        search_lon=MagicMock(),
        user_let=MagicMock(),
        user_lon=MagicMock(),
        coded_style=MagicMock(),
    )
    pass


def test_generate_yandex_maps_place_link():
    from communicate import main

    res = main.generate_yandex_maps_place_link(lat=MagicMock(), lon=MagicMock(), param=MagicMock())
    pass


def test_get_basic_update_parameters():
    from communicate import main

    res = main.get_basic_update_parameters(update=MagicMock())
    pass


def test_get_coordinates_from_string():
    from communicate import main

    res = main.get_coordinates_from_string(
        got_message=MagicMock(), lat_placeholder=MagicMock(), lon_placeholder=MagicMock()
    )
    pass


def test_get_last_bot_message_id():
    from communicate import main

    res = main.get_last_bot_message_id(response=MagicMock())
    pass


def test_get_last_bot_msg():
    from communicate import main

    res = main.get_last_bot_msg(cur=MagicMock(), user_id=MagicMock())
    pass


def test_get_last_user_inline_dialogue():
    from communicate import main

    res = main.get_last_user_inline_dialogue(cur=MagicMock(), user_id=1)
    pass


def test_get_param_if_exists():
    from communicate import main

    res = main.get_param_if_exists(upd=MagicMock(), func_input=MagicMock())
    pass


def test_get_search_follow_mode():
    from communicate import main

    res = main.get_search_follow_mode(cur=MagicMock(), user_id=1)
    pass


def test_get_secrets():
    from communicate import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_get_the_update():
    from communicate import main

    res = main.get_the_update(bot=MagicMock(), request=MagicMock())
    pass


def test_get_user_reg_folders_preferences():
    from communicate import main

    res = main.get_user_reg_folders_preferences(cur=MagicMock(), user_id=MagicMock())
    pass


def test_get_user_role():
    from communicate import main

    res = main.get_user_role(cur=MagicMock(), user_id=MagicMock())
    pass


def test_get_user_sys_roles():
    from communicate import main

    res = main.get_user_sys_roles(cur=MagicMock(), user_id=MagicMock())
    pass


def test_if_user_enables():
    from communicate import main

    res = main.if_user_enables(callback=MagicMock())
    pass


def test_inline_processing():
    from communicate import main

    res = main.inline_processing(cur=MagicMock(), response=MagicMock(), params=MagicMock())
    pass


def test_leave_chat_async():
    from communicate import main

    res = main.leave_chat_async(context=MagicMock())
    pass


def test_main():
    from communicate import main

    res = main.main(request=MagicMock())
    pass


def test_make_api_call():
    from communicate import main

    res = main.make_api_call(method='foo', bot_api_token='foo', params={}, call_context=MagicMock())
    pass


def test_manage_age():
    from communicate import main

    with pytest.raises(Exception):
        res = main.manage_age(cur=MagicMock(), user_id=MagicMock(), user_input=MagicMock())
    pass


def test_manage_if_moscow():
    from communicate import main

    res = main.manage_if_moscow(
        cur=MagicMock(),
        user_id=MagicMock(),
        username=MagicMock(),
        got_message=MagicMock(),
        b_reg_moscow=MagicMock(),
        b_reg_not_moscow=MagicMock(),
        reply_markup=MagicMock(),
        keyboard_fed_dist_set=MagicMock(),
        bot_message=MagicMock(),
        user_role=MagicMock(),
    )
    pass


def test_manage_linking_to_forum():
    from communicate import main

    res = main.manage_linking_to_forum(
        cur=MagicMock(),
        got_message=MagicMock(),
        user_id=MagicMock(),
        b_set_forum_nick=MagicMock(),
        b_back_to_start=MagicMock(),
        bot_request_bfr_usr_msg=MagicMock(),
        b_admin_menu=MagicMock(),
        b_test_menu=MagicMock(),
        b_yes_its_me=MagicMock(),
        b_no_its_not_me=MagicMock(),
        b_settings=MagicMock(),
        reply_markup_main=MagicMock(),
    )
    pass


def test_manage_radius():
    from communicate import main

    res = main.manage_radius(
        cur=MagicMock(),
        user_id=MagicMock(),
        user_input=MagicMock(),
        b_menu=MagicMock(),
        b_act=MagicMock(),
        b_deact=MagicMock(),
        b_change=MagicMock(),
        b_back=MagicMock(),
        b_home_coord=MagicMock(),
        expect_before=MagicMock(),
    )
    pass


def test_manage_search_follow_mode():
    from communicate import main

    with pytest.raises(Exception):
        res = main.manage_search_follow_mode(
            cur=MagicMock(),
            user_id=MagicMock(),
            user_callback=MagicMock(),
            callback_id=MagicMock(),
            callback_query=MagicMock(),
            bot_token=MagicMock(),
        )
    pass


def test_manage_search_whiteness():
    from communicate import main

    with pytest.raises(Exception):
        res = main.manage_search_whiteness(
            cur=MagicMock(),
            user_id=MagicMock(),
            user_callback=MagicMock(),
            callback_id=MagicMock(),
            callback_query=MagicMock(),
            bot_token=MagicMock(),
        )
    pass


def test_manage_topic_type():
    from communicate import main

    with pytest.raises(Exception):
        res = main.manage_topic_type(
            cur=MagicMock(),
            user_id=MagicMock(),
            user_input=MagicMock(),
            b=MagicMock(),
            user_callback=MagicMock(),
            callback_id=MagicMock(),
            bot_token=MagicMock(),
            callback_query_msg_id=MagicMock(),
        )
    pass


def test_prepare_message_for_async():
    from communicate import main

    res = main.prepare_message_for_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_prepare_message_for_leave_chat_async():
    from communicate import main

    res = main.prepare_message_for_leave_chat_async(user_id=MagicMock())
    pass


def test_process_block_unblock_user():
    from communicate import main

    res = main.process_block_unblock_user(user_id=MagicMock(), user_new_status=MagicMock())
    pass


def test_process_leaving_chat_async():
    from communicate import main

    with pytest.raises(Exception):
        res = main.process_leaving_chat_async(user_id=MagicMock())
    pass


def test_process_response_of_api_call():
    from communicate import main

    res = main.process_response_of_api_call(user_id=MagicMock(), response=MagicMock(), call_context=MagicMock())
    pass


def test_process_sending_message_async():
    from communicate import main

    with pytest.raises(Exception):
        res = main.process_sending_message_async(user_id=MagicMock(), data=MagicMock())
    pass


def test_process_unneeded_messages():
    from communicate import main

    res = main.process_unneeded_messages(
        update=MagicMock(),
        user_id=MagicMock(),
        timer_changed=MagicMock(),
        photo=MagicMock(),
        document=MagicMock(),
        voice=MagicMock(),
        sticker=MagicMock(),
        channel_type=MagicMock(),
        contact=MagicMock(),
        inline_query=MagicMock(),
    )
    pass


def test_process_user_coordinates():
    from communicate import main

    with pytest.raises(Exception):
        res = main.process_user_coordinates(
            cur=MagicMock(),
            user_id=MagicMock(),
            user_latitude=MagicMock(),
            user_longitude=MagicMock(),
            b_coords_check=MagicMock(),
            b_coords_del=MagicMock(),
            b_back_to_start=MagicMock(),
            bot_request_aft_usr_msg=MagicMock(),
        )
    pass


def test_run_onboarding():
    from communicate import main

    res = main.run_onboarding(
        user_id=MagicMock(), username=MagicMock(), onboarding_step_id=MagicMock(), got_message=MagicMock()
    )
    pass


def test_save_bot_reply_to_user():
    from communicate import main

    res = main.save_bot_reply_to_user(cur=MagicMock(), user_id=MagicMock(), bot_message=MagicMock())
    pass


def test_save_last_user_inline_dialogue():
    from communicate import main

    res = main.save_last_user_inline_dialogue(cur=MagicMock(), user_id=1, message_id=1)
    pass


def test_save_new_user():
    from communicate import main

    with pytest.raises(Exception):
        res = main.save_new_user(user_id=MagicMock(), username=MagicMock())
    pass


def test_save_onboarding_step():
    from communicate import main

    with pytest.raises(Exception):
        res = main.save_onboarding_step(user_id=MagicMock(), username=MagicMock(), step=MagicMock())
    pass


def test_save_preference():
    from communicate import main

    res = main.save_preference(cur=MagicMock(), user_id=MagicMock(), preference=MagicMock())
    pass


def test_save_user_coordinates():
    from communicate import main

    res = main.save_user_coordinates(
        cur=MagicMock(), user_id=MagicMock(), input_latitude=MagicMock(), input_longitude=MagicMock()
    )
    pass


def test_save_user_message_to_bot():
    from communicate import main

    res = main.save_user_message_to_bot(cur=MagicMock(), user_id=MagicMock(), got_message=MagicMock())
    pass


def test_save_user_pref_role():
    from communicate import main

    res = main.save_user_pref_role(cur=MagicMock(), user_id=MagicMock(), role_desc=MagicMock())
    pass


def test_save_user_pref_topic_type():
    from communicate import main

    res = main.save_user_pref_topic_type(
        cur=MagicMock(), user_id=MagicMock(), pref_id=MagicMock(), user_role=MagicMock()
    )
    pass


def test_save_user_pref_urgency():
    from communicate import main

    res = main.save_user_pref_urgency(
        cur=MagicMock(),
        user_id=MagicMock(),
        urgency_value=MagicMock(),
        b_pref_urgency_highest=MagicMock(),
        b_pref_urgency_high=MagicMock(),
        b_pref_urgency_medium=MagicMock(),
        b_pref_urgency_low=MagicMock(),
    )
    pass


def test_search_button_row_ikb():
    from communicate import main

    res = main.search_button_row_ikb(
        search_following_mode=MagicMock(),
        search_status=MagicMock(),
        search_id=MagicMock(),
        search_display_name=MagicMock(),
        url=MagicMock(),
    )
    pass


def test_send_callback_answer_to_api():
    from communicate import main

    with pytest.raises(Exception):
        res = main.send_callback_answer_to_api(
            bot_token=MagicMock(), callback_query_id=MagicMock(), message=MagicMock()
        )
    pass


def test_send_message_async():
    from communicate import main

    res = main.send_message_async(context=MagicMock())
    pass


def test_send_message_to_api():
    from communicate import main

    with pytest.raises(Exception):
        res = main.send_message_to_api(
            bot_token=MagicMock(), user_id=MagicMock(), message=MagicMock(), params=MagicMock()
        )
    pass


def test_set_search_follow_mode():
    from communicate import main

    res = main.set_search_follow_mode(cur=MagicMock(), user_id=1, new_value=MagicMock())
    pass


def test_show_user_coordinates():
    from communicate import main

    res = main.show_user_coordinates(cur=MagicMock(), user_id=MagicMock())
    pass


def test_sql_connect_by_psycopg2():
    from communicate import main

    res = main.sql_connect_by_psycopg2()
    pass


def test_time_counter_since_search_start():
    from communicate import main

    with pytest.raises(Exception):
        res = main.time_counter_since_search_start(start_time=MagicMock())
    pass


def test_update_and_download_list_of_regions():
    from communicate import main

    res = main.update_and_download_list_of_regions(
        cur=MagicMock(),
        user_id=MagicMock(),
        got_message=MagicMock(),
        b_menu_set_region=MagicMock(),
        b_fed_dist_pick_other=MagicMock(),
    )
    pass
