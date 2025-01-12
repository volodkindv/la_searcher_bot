from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_evaluate_city_locations():
    from api_get_active_searches import main

    with pytest.raises(Exception):
        res = main.evaluate_city_locations(city_locations=MagicMock())
    pass


def test_get_list_of_active_searches_from_db():
    from api_get_active_searches import main

    res = main.get_list_of_active_searches_from_db(request=MagicMock())
    pass


def test_get_list_of_allowed_apps():
    from api_get_active_searches import main

    res = main.get_list_of_allowed_apps()
    pass


def test_main():
    from api_get_active_searches import main

    res = main.main(request=MagicMock())
    pass


def test_save_user_statistics_to_db():
    from api_get_active_searches import main

    res = main.save_user_statistics_to_db(user_input=MagicMock(), response=MagicMock())
    pass


def test_sql_connect_by_psycopg2():
    from api_get_active_searches import main

    res = main.sql_connect_by_psycopg2()
    pass


def test_time_counter_since_search_start():
    from api_get_active_searches import main

    with pytest.raises(Exception):
        res = main.time_counter_since_search_start(start_time=MagicMock())
    pass


def test_verify_json_validity():
    from api_get_active_searches import main

    res = main.verify_json_validity(user_input=MagicMock(), list_of_allowed_apps=MagicMock())
    pass
