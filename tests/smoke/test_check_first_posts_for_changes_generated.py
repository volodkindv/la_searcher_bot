from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from check_first_posts_for_changes import main


def test_define_topic_visibility_by_content():
    res = main.define_topic_visibility_by_content(content='foo')
    pass


def test_define_topic_visibility_by_topic_id():
    res = main.define_topic_visibility_by_topic_id(search_num=MagicMock())
    pass


def test_get_status_from_content_and_send_to_topic_management():
    res = main.get_status_from_content_and_send_to_topic_management(topic_id='foo', act_content='foo')
    pass


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_make_api_call():
    res = main.make_api_call(function='foo', data={})
    pass


def test_parse_search():
    res = main.parse_search(search_num=MagicMock())
    pass


def test_sql_connect():
    res = main.sql_connect()
    pass


def test_update_first_posts_and_statuses():
    res = main.update_first_posts_and_statuses()
    pass


def test_update_one_topic_visibility():
    res = main.update_one_topic_visibility(search_id=MagicMock())
    pass


def test_update_visibility_for_one_hidden_topic():
    res = main.update_visibility_for_one_hidden_topic()
    pass
