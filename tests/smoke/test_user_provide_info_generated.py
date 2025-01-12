from unittest.mock import MagicMock

from user_provide_info import main


def test_evaluate_city_locations():
    res = main.evaluate_city_locations(city_locations=MagicMock())
    pass


def test_get_user_data_from_db():
    res = main.get_user_data_from_db(user_id=1)
    pass


def test_main():
    res = main.main(request=MagicMock())
    pass


def test_save_user_statistics_to_db():
    res = main.save_user_statistics_to_db(user_id=1, response=False)
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


def test_unquote():
    res = main.unquote(string=MagicMock(), encoding=MagicMock(), errors=MagicMock())
    pass


def test_verify_telegram_data():
    res = main.verify_telegram_data(user_input=MagicMock(), token=MagicMock())
    pass


def test_verify_telegram_data_json():
    res = main.verify_telegram_data_json(user_input=MagicMock(), token=MagicMock())
    pass


def test_verify_telegram_data_string():
    res = main.verify_telegram_data_string(user_input=MagicMock(), token=MagicMock())
    pass
