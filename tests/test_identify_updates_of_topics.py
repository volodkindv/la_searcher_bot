from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from _dependencies.commons import sql_connect_by_psycopg2
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

    with (
        sql_connect_by_psycopg2() as db,
        patch.object(main, 'requests_session', requests.Session()),
        patch.object(main.requests_session, 'get') as mock_http,
        patch.object(main, 'make_api_call', fake_api_call),
    ):
        mock_http.return_value.content = Path('tests/fixtures/forum_folder_276.html').read_bytes()

        forum_search_folder_id = 276
        summaries, details = main.parse_one_folder(db, forum_search_folder_id)
        assert summaries == [
            ['Жив Иванов Иван, 10 лет, ЗАО, г. Москва', 29],
            ['Пропал Петров Петр Петрович, 48 лет, ЗелАО, г. Москва - Тверская обл.', 116],
        ]
        assert len(details) == 2
