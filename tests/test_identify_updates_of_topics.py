from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from _dependencies.commons import sql_connect_by_psycopg2, sqlalchemy_get_pool
from identify_updates_of_topics import main
from tests.common import get_event_with_data
from title_recognize.main import recognize_title


def test_main():
    data = 'foo'
    with pytest.raises(ValueError):
        main.main(get_event_with_data(data), 'context')
    assert True


def test_get_cordinates():
    data = 'Москва, Ярославское шоссе 123'
    db = main.sql_connect()
    with patch('identify_updates_of_topics.main.rate_limit_for_api'):
        res = main.get_coordinates(db, data)
    assert res == (None, None)


def test_rate_limit_for_api():
    data = 'Москва, Ярославское шоссе 123'
    db = main.sql_connect()
    main.rate_limit_for_api(db, data)


def test_get_the_list_of_ignored_folders():
    res = main.get_the_list_of_ignored_folders(main.sql_connect())
    assert not res


def test_parse_one_folder():
    def fake_api_call(function: str, data: dict):
        reco_data = recognize_title(data['title'], None)
        return {'status': 'ok', 'recognition': reco_data}

    pool = sqlalchemy_get_pool(10, 10)
    with (
        patch.object(main, 'requests_session', requests.Session()),
        patch.object(main.requests_session, 'get') as mock_http,
        patch.object(main, 'make_api_call', fake_api_call),
    ):
        mock_http.return_value.content = Path('tests/fixtures/forum_folder_276.html').read_bytes()

        forum_search_folder_id = 276
        summaries, details = main.parse_one_folder(pool, forum_search_folder_id)
        assert summaries == [
            ['Жив Иванов Иван, 10 лет, ЗАО, г. Москва', 29],
            ['Пропал Петров Петр Петрович, 48 лет, ЗелАО, г. Москва - Тверская обл.', 116],
        ]
        assert len(details) == 2


def test_process_one_folder():
    def fake_api_call(function: str, data: dict):
        reco_data = recognize_title(data['title'], None)
        return {'status': 'ok', 'recognition': reco_data}

    pool = sqlalchemy_get_pool(10, 10)
    with (
        patch.object(main, 'requests_session', requests.Session()),
        patch.object(main.requests_session, 'get') as mock_http,
        patch.object(main, 'make_api_call', fake_api_call),
        patch.object(main, 'read_snapshot_from_cloud_storage', Mock(return_value='foo')),
        patch.object(main, 'write_snapshot_to_cloud_storage'),
        patch.object(main, 'parse_search_profile', Mock(return_value='foo')),
    ):
        mock_http.return_value.content = Path('tests/fixtures/forum_folder_276.html').read_bytes()

        forum_search_folder_id = 276
        update_trigger, changed_ids = main.process_one_folder(pool, forum_search_folder_id)
        assert update_trigger is True


def test_main_full_scenario():
    def fake_api_call(function: str, data: dict):
        reco_data = recognize_title(data['title'], None)
        return {'status': 'ok', 'recognition': reco_data}

    with (
        patch.object(main, 'requests_session', requests.Session()),
        patch.object(main.requests_session, 'get') as mock_http,
        patch.object(main, 'make_api_call', fake_api_call),
        patch.object(main, 'read_snapshot_from_cloud_storage', Mock(return_value='foo')),
        patch.object(main, 'write_snapshot_to_cloud_storage'),
        patch.object(main, 'parse_search_profile', Mock(return_value='foo')),
        patch('compose_notifications.main.check_if_need_compose_more'),  # avoid recursion in tests
    ):
        mock_http.return_value.content = Path('tests/fixtures/forum_folder_276.html').read_bytes()

        forum_search_folder_id = 276
        data = [(forum_search_folder_id,)]
        main.main(get_event_with_data(str(data)), 'context')
