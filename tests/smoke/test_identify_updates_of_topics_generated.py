from unittest.mock import MagicMock

from identify_updates_of_topics import main


def test_define_start_time_of_search():
    res = main.define_start_time_of_search(blocks=MagicMock())
    pass


def test_generate_random_function_id():
    res = main.generate_random_function_id()
    pass


def test_get_coordinates():
    res = main.get_coordinates(db=MagicMock(), address=MagicMock())
    pass


def test_get_last_api_call_time_from_psql():
    res = main.get_last_api_call_time_from_psql(db=MagicMock(), geocoder=MagicMock())
    pass


def test_get_the_list_of_ignored_folders():
    res = main.get_the_list_of_ignored_folders(db=MagicMock())
    pass


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_make_api_call():
    res = main.make_api_call(function=MagicMock(), data=MagicMock())
    pass


def test_notify_admin():
    res = main.notify_admin(message=MagicMock())
    pass


def test_parse_coordinates():
    res = main.parse_coordinates(db=MagicMock(), search_num=MagicMock())
    pass


def test_parse_one_comment():
    res = main.parse_one_comment(db=MagicMock(), search_num=MagicMock(), comment_num=MagicMock())
    pass


def test_parse_one_folder():
    res = main.parse_one_folder(db=MagicMock(), folder_id=MagicMock())
    pass


def test_parse_search_profile():
    res = main.parse_search_profile(search_num=MagicMock())
    pass


def test_process_one_folder():
    res = main.process_one_folder(db=MagicMock(), folder_to_parse=MagicMock())
    pass


def test_process_pubsub_message():
    res = main.process_pubsub_message(event=MagicMock())
    pass


def test_profile_get_managers():
    res = main.profile_get_managers(text_of_managers=MagicMock())
    pass


def test_profile_get_type_of_activity():
    res = main.profile_get_type_of_activity(text_of_activity=MagicMock())
    pass


def test_publish_to_pubsub():
    res = main.publish_to_pubsub(topic_name=MagicMock(), message=MagicMock())
    pass


def test_rate_limit_for_api():
    res = main.rate_limit_for_api(db=MagicMock(), geocoder=MagicMock())
    pass


def test_read_snapshot_from_cloud_storage():
    res = main.read_snapshot_from_cloud_storage(bucket_to_read=MagicMock(), folder_num=MagicMock())
    pass


def test_read_yaml_from_cloud_storage():
    res = main.read_yaml_from_cloud_storage(bucket_to_read=MagicMock(), folder_num=MagicMock())
    pass


def test_save_function_into_register():
    res = main.save_function_into_register(
        db=MagicMock(), context=MagicMock(), start_time=MagicMock(), function_id=MagicMock(), change_log_ids=MagicMock()
    )
    pass


def test_save_last_api_call_time_to_psql():
    res = main.save_last_api_call_time_to_psql(db=MagicMock(), geocoder=MagicMock())
    pass


def test_set_cloud_storage():
    res = main.set_cloud_storage(bucket_name=MagicMock(), folder_num=MagicMock())
    pass


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass


def test_sql_connect():
    res = main.sql_connect()
    pass


def test_update_change_log_and_searches():
    res = main.update_change_log_and_searches(db=MagicMock(), folder_num=MagicMock())
    pass


def test_update_coordinates():
    res = main.update_coordinates(db=MagicMock(), list_of_search_objects=MagicMock())
    pass


def test_visibility_check():
    res = main.visibility_check(r=MagicMock(), topic_id=MagicMock())
    pass


def test_write_snapshot_to_cloud_storage():
    res = main.write_snapshot_to_cloud_storage(
        bucket_to_write=MagicMock(), what_to_write=MagicMock(), folder_num=MagicMock()
    )
    pass
