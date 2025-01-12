from datetime import date, datetime
from unittest.mock import MagicMock

from api_get_active_searches import main


def test_evaluate_city_locations():
    res = main.evaluate_city_locations(city_locations=MagicMock())
    pass


def test_get_list_of_active_searches_from_db():
    res = main.get_list_of_active_searches_from_db(request=MagicMock())
    pass


def test_get_list_of_allowed_apps():
    res = main.get_list_of_allowed_apps()
    pass


def test_main():
    res = main.main(request=MagicMock())
    pass


def test_save_user_statistics_to_db():
    res = main.save_user_statistics_to_db(user_input=MagicMock(), response=MagicMock())
    pass


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass


def test_sql_connect_by_psycopg2():
    res = main.sql_connect_by_psycopg2()
    pass


def test_time_counter_since_search_start():
    res = main.time_counter_since_search_start(start_time=MagicMock())
    pass


def test_verify_json_validity():
    res = main.verify_json_validity(user_input=MagicMock(), list_of_allowed_apps=MagicMock())
    pass
