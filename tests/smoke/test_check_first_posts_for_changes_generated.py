from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_define_topic_visibility_by_content():
    from check_first_posts_for_changes import main

    with pytest.raises(Exception):
        res = main.define_topic_visibility_by_content(content=MagicMock())
    pass


def test_define_topic_visibility_by_topic_id():
    from check_first_posts_for_changes import main

    res = main.define_topic_visibility_by_topic_id(search_num=MagicMock())
    pass


def test_get_secrets():
    from check_first_posts_for_changes import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_get_status_from_content_and_send_to_topic_management():
    from check_first_posts_for_changes import main

    with pytest.raises(Exception):
        res = main.get_status_from_content_and_send_to_topic_management(topic_id=MagicMock(), act_content=MagicMock())
    pass


def test_main():
    from check_first_posts_for_changes import main

    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_make_api_call():
    from check_first_posts_for_changes import main

    res = main.make_api_call(function='foo', data={})
    pass


def test_parse_search():
    from check_first_posts_for_changes import main

    res = main.parse_search(search_num=MagicMock())
    pass


def test_sql_connect():
    from check_first_posts_for_changes import main

    res = main.sql_connect()
    pass


def test_update_first_posts_and_statuses():
    from check_first_posts_for_changes import main

    res = main.update_first_posts_and_statuses()
    pass


def test_update_one_topic_visibility():
    from check_first_posts_for_changes import main

    res = main.update_one_topic_visibility(search_id=MagicMock())
    pass


def test_update_visibility_for_one_hidden_topic():
    from check_first_posts_for_changes import main

    res = main.update_visibility_for_one_hidden_topic()
    pass
