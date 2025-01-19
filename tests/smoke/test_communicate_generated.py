import pytest

from communicate import main
from tests.common import run_smoke


def test_add_user_sys_role():
    res = run_smoke(main.add_user_sys_role)
    pass


def test_age_writer():
    res = run_smoke(main.age_writer)
    pass


def test_api_callback_edit_inline_keyboard():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.api_callback_edit_inline_keyboard)
    pass


def test_check_if_new_user():
    res = run_smoke(main.check_if_new_user)
    pass


def test_check_if_user_has_no_regions():
    res = run_smoke(main.check_if_user_has_no_regions)
    pass


def test_check_onboarding_step():
    res = run_smoke(main.check_onboarding_step)
    pass


def test_compose_full_message_on_list_of_searches():
    res = run_smoke(main.compose_full_message_on_list_of_searches)
    pass


def test_compose_full_message_on_list_of_searches_ikb():
    res = run_smoke(main.compose_full_message_on_list_of_searches_ikb)
    pass


def test_compose_msg_on_active_searches_in_one_reg():
    res = run_smoke(main.compose_msg_on_active_searches_in_one_reg)
    pass


def test_compose_msg_on_active_searches_in_one_reg_ikb():
    res = run_smoke(main.compose_msg_on_active_searches_in_one_reg_ikb)
    pass


def test_compose_msg_on_all_last_searches():
    res = run_smoke(main.compose_msg_on_all_last_searches)
    pass


def test_compose_msg_on_all_last_searches_ikb():
    res = run_smoke(main.compose_msg_on_all_last_searches_ikb)
    pass


def test_compose_msg_on_user_setting_fullness():
    res = run_smoke(main.compose_msg_on_user_setting_fullness)
    pass


def test_compose_user_preferences_message():
    res = run_smoke(main.compose_user_preferences_message)
    pass


def test_delete_last_user_inline_dialogue():
    res = run_smoke(main.delete_last_user_inline_dialogue)
    pass


def test_delete_user_coordinates():
    res = run_smoke(main.delete_user_coordinates)
    pass


def test_delete_user_sys_role():
    res = run_smoke(main.delete_user_sys_role)
    pass


def test_distance_to_search():
    res = run_smoke(main.distance_to_search)
    pass


def test_generate_yandex_maps_place_link():
    res = run_smoke(main.generate_yandex_maps_place_link)
    pass


def test_get_basic_update_parameters():
    res = run_smoke(main.get_basic_update_parameters)
    pass


def test_get_coordinates_from_string():
    res = run_smoke(main.get_coordinates_from_string)
    pass


def test_get_last_bot_message_id():
    res = run_smoke(main.get_last_bot_message_id)
    pass


def test_get_last_bot_msg():
    res = run_smoke(main.get_last_bot_msg)
    pass


def test_get_last_user_inline_dialogue():
    res = run_smoke(main.get_last_user_inline_dialogue)
    pass


def test_get_param_if_exists():
    res = run_smoke(main.get_param_if_exists)
    pass


def test_get_search_follow_mode():
    res = run_smoke(main.get_search_follow_mode)
    pass


def test_get_the_update():
    res = run_smoke(main.get_the_update)
    pass


def test_get_user_reg_folders_preferences():
    res = run_smoke(main.get_user_reg_folders_preferences)
    pass


def test_get_user_role():
    res = run_smoke(main.get_user_role)
    pass


def test_get_user_sys_roles():
    res = run_smoke(main.get_user_sys_roles)
    pass


def test_if_user_enables():
    res = run_smoke(main.if_user_enables)
    pass


def test_inline_processing():
    res = run_smoke(main.inline_processing)
    pass


def test_leave_chat_async():
    res = run_smoke(main.leave_chat_async)
    pass


def test_main():
    res = run_smoke(main.main)
    pass


def test_make_api_call():
    res = run_smoke(main.make_api_call)
    pass


def test_manage_age():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.manage_age)
    pass


def test_manage_if_moscow():
    res = run_smoke(main.manage_if_moscow)
    pass


def test_manage_linking_to_forum():
    res = run_smoke(main.manage_linking_to_forum)
    pass


def test_manage_radius():
    res = run_smoke(main.manage_radius)
    pass


def test_manage_search_follow_mode():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.manage_search_follow_mode)
    pass


def test_manage_search_whiteness():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.manage_search_whiteness)
    pass


def test_manage_topic_type():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.manage_topic_type)
    pass


def test_prepare_message_for_async():
    res = run_smoke(main.prepare_message_for_async)
    pass


def test_prepare_message_for_leave_chat_async():
    res = run_smoke(main.prepare_message_for_leave_chat_async)
    pass


def test_process_block_unblock_user():
    res = run_smoke(main.process_block_unblock_user)
    pass


def test_process_leaving_chat_async():
    res = run_smoke(main.process_leaving_chat_async)
    pass


def test_process_response_of_api_call():
    res = run_smoke(main.process_response_of_api_call)
    pass


def test_process_sending_message_async():
    res = run_smoke(main.process_sending_message_async)
    pass


def test_process_unneeded_messages():
    res = run_smoke(main.process_unneeded_messages)
    pass


def test_process_update():
    res = run_smoke(main.process_update)
    pass


def test_process_user_coordinates():
    res = run_smoke(main.process_user_coordinates)
    pass


def test_run_onboarding():
    res = run_smoke(main.run_onboarding)
    pass


def test_save_bot_reply_to_user():
    res = run_smoke(main.save_bot_reply_to_user)
    pass


def test_save_last_user_inline_dialogue():
    res = run_smoke(main.save_last_user_inline_dialogue)
    pass


def test_save_new_user():
    res = run_smoke(main.save_new_user)
    pass


def test_save_onboarding_step():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.save_onboarding_step)
    pass


def test_save_preference():
    res = run_smoke(main.save_preference)
    pass


def test_save_user_coordinates():
    res = run_smoke(main.save_user_coordinates)
    pass


def test_save_user_message_to_bot():
    res = run_smoke(main.save_user_message_to_bot)
    pass


def test_save_user_pref_role():
    res = run_smoke(main.save_user_pref_role)
    pass


def test_save_user_pref_topic_type():
    res = run_smoke(main.save_user_pref_topic_type)
    pass


def test_save_user_pref_urgency():
    res = run_smoke(main.save_user_pref_urgency)
    pass


def test_search_button_row_ikb():
    res = run_smoke(main.search_button_row_ikb)
    pass


def test_send_callback_answer_to_api():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.send_callback_answer_to_api)
    pass


def test_send_message_async():
    res = run_smoke(main.send_message_async)
    pass


def test_send_message_to_api():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.send_message_to_api)
    pass


def test_set_search_follow_mode():
    res = run_smoke(main.set_search_follow_mode)
    pass


def test_show_user_coordinates():
    res = run_smoke(main.show_user_coordinates)
    pass


def test_update_and_download_list_of_regions():
    res = run_smoke(main.update_and_download_list_of_regions)
    pass
