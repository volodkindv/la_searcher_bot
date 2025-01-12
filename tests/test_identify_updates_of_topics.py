from unittest.mock import patch

import pytest

from identify_updates_of_topics import main
from tests.common import get_event_with_data


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


def test_rate_limit_for_api(use_real_db: bool):
    data = 'Москва, Ярославское шоссе 123'
    db = main.sql_connect()
    if use_real_db:
        main.rate_limit_for_api(db, data)
    else:
        with pytest.raises(TypeError):
            main.rate_limit_for_api(db, data)
    assert True


def test_get_the_list_of_ignored_folders():
    res = main.get_the_list_of_ignored_folders(main.sql_connect())
    assert not res
