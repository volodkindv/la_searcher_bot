from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_age_writer():
    from identify_updates_of_first_posts import main

    res = main.age_writer(age=MagicMock())
    pass


def test_compose_diff_message():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.compose_diff_message(curr_list=MagicMock(), prev_list=MagicMock())
    pass


def test_generate_random_function_id():
    from identify_updates_of_first_posts import main

    res = main.generate_random_function_id()
    pass


def test_get_compressed_first_post():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.get_compressed_first_post(initial_text=MagicMock())
    pass


def test_get_field_trip_details_from_text():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.get_field_trip_details_from_text(text=MagicMock())
    pass


def test_get_secrets():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_get_the_list_of_coords_out_of_text():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.get_the_list_of_coords_out_of_text(initial_text=MagicMock())
    pass


def test_main():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_parse_search_folder():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.parse_search_folder(search_num=MagicMock())
    pass


def test_process_first_page_comparison():
    from identify_updates_of_first_posts import main

    res = main.process_first_page_comparison(
        conn=MagicMock(),
        search_id=MagicMock(),
        first_page_content_prev=MagicMock(),
        first_page_content_curr=MagicMock(),
    )
    pass


def test_process_pubsub_message():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.process_pubsub_message(event=MagicMock())
    pass


def test_save_function_into_register():
    from identify_updates_of_first_posts import main

    res = main.save_function_into_register(
        conn=MagicMock(),
        context=MagicMock(),
        start_time=MagicMock(),
        function_id=MagicMock(),
        change_log_ids=MagicMock(),
    )
    pass


def test_save_new_record_into_change_log():
    from identify_updates_of_first_posts import main

    res = main.save_new_record_into_change_log(
        conn=MagicMock(),
        search_id=MagicMock(),
        coords_change_list=MagicMock(),
        changed_field=MagicMock(),
        change_type=MagicMock(),
    )
    pass


def test_split_text_to_deleted_and_regular_parts():
    from identify_updates_of_first_posts import main

    with pytest.raises(Exception):
        res = main.split_text_to_deleted_and_regular_parts(text=MagicMock())
    pass


def test_sql_connect():
    from identify_updates_of_first_posts import main

    res = main.sql_connect()
    pass
