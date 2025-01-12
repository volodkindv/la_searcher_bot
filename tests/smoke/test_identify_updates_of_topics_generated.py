from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_define_start_time_of_search():
    from identify_updates_of_topics import main

    res = main.define_start_time_of_search(blocks=MagicMock())
    pass


def test_generate_random_function_id():
    from identify_updates_of_topics import main

    res = main.generate_random_function_id()
    pass


def test_get_coordinates():
    from identify_updates_of_topics import main

    res = main.get_coordinates(db=MagicMock(), address=MagicMock())
    pass


def test_get_last_api_call_time_from_psql():
    from identify_updates_of_topics import main

    res = main.get_last_api_call_time_from_psql(db=MagicMock(), geocoder='foo')
    pass


def test_get_secrets():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_get_the_list_of_ignored_folders():
    from identify_updates_of_topics import main

    res = main.get_the_list_of_ignored_folders(db=MagicMock())
    pass


def test_main():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_make_api_call():
    from identify_updates_of_topics import main

    res = main.make_api_call(function='foo', data={})
    pass


def test_parse_coordinates():
    from identify_updates_of_topics import main

    res = main.parse_coordinates(db=MagicMock(), search_num=MagicMock())
    pass


def test_parse_one_comment():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.parse_one_comment(db=MagicMock(), search_num=MagicMock(), comment_num=MagicMock())
    pass


def test_parse_one_folder():
    from identify_updates_of_topics import main

    res = main.parse_one_folder(db=MagicMock(), folder_id=MagicMock())
    pass


def test_parse_search_profile():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.parse_search_profile(search_num=MagicMock())
    pass


def test_process_one_folder():
    from identify_updates_of_topics import main

    res = main.process_one_folder(db=MagicMock(), folder_to_parse=MagicMock())
    pass


def test_process_pubsub_message():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.process_pubsub_message(event=MagicMock())
    pass


def test_profile_get_managers():
    from identify_updates_of_topics import main

    res = main.profile_get_managers(text_of_managers=MagicMock())
    pass


def test_profile_get_type_of_activity():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.profile_get_type_of_activity(text_of_activity=MagicMock())
    pass


def test_rate_limit_for_api():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.rate_limit_for_api(db=MagicMock(), geocoder='foo')
    pass


def test_read_snapshot_from_cloud_storage():
    from identify_updates_of_topics import main

    res = main.read_snapshot_from_cloud_storage(bucket_to_read=MagicMock(), folder_num=MagicMock())
    pass


def test_read_yaml_from_cloud_storage():
    from identify_updates_of_topics import main

    res = main.read_yaml_from_cloud_storage(bucket_to_read=MagicMock(), folder_num=MagicMock())
    pass


def test_save_function_into_register():
    from identify_updates_of_topics import main

    res = main.save_function_into_register(
        db=MagicMock(), context=MagicMock(), start_time=MagicMock(), function_id=MagicMock(), change_log_ids=MagicMock()
    )
    pass


def test_save_last_api_call_time_to_psql():
    from identify_updates_of_topics import main

    res = main.save_last_api_call_time_to_psql(db=MagicMock(), geocoder='foo')
    pass


def test_set_cloud_storage():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.set_cloud_storage(bucket_name=MagicMock(), folder_num=MagicMock())
    pass


def test_sql_connect():
    from identify_updates_of_topics import main

    res = main.sql_connect()
    pass


def test_update_change_log_and_searches():
    from identify_updates_of_topics import main

    res = main.update_change_log_and_searches(db=MagicMock(), folder_num=MagicMock())
    pass


def test_update_coordinates():
    from identify_updates_of_topics import main

    res = main.update_coordinates(db=MagicMock(), list_of_search_objects=MagicMock())
    pass


def test_visibility_check():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.visibility_check(r=MagicMock(), topic_id=MagicMock())
    pass


def test_write_snapshot_to_cloud_storage():
    from identify_updates_of_topics import main

    with pytest.raises(Exception):
        res = main.write_snapshot_to_cloud_storage(
            bucket_to_write=MagicMock(), what_to_write=MagicMock(), folder_num=MagicMock()
        )
    pass
