from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_evaluate_city_locations():
    from user_provide_info import main

    with pytest.raises(Exception):
        res = main.evaluate_city_locations(city_locations=MagicMock())
    pass


def test_get_secrets():
    from user_provide_info import main

    with pytest.raises(Exception):
        res = main.get_secrets(secret_request=MagicMock())
    pass


def test_get_user_data_from_db():
    from user_provide_info import main

    res = main.get_user_data_from_db(user_id=1)
    pass


def test_main():
    from user_provide_info import main

    res = main.main(request=MagicMock())
    pass


def test_save_user_statistics_to_db():
    from user_provide_info import main

    res = main.save_user_statistics_to_db(user_id=1, response=False)
    pass


def test_sql_connect_by_psycopg2():
    from user_provide_info import main

    res = main.sql_connect_by_psycopg2()
    pass


def test_time_counter_since_search_start():
    from user_provide_info import main

    with pytest.raises(Exception):
        res = main.time_counter_since_search_start(start_time=MagicMock())
    pass


def test_unquote():
    from user_provide_info import main

    res = main.unquote(string=MagicMock(), encoding=MagicMock(), errors=MagicMock())
    pass


def test_verify_telegram_data():
    from user_provide_info import main

    res = main.verify_telegram_data(user_input=MagicMock(), token=MagicMock())
    pass


def test_verify_telegram_data_json():
    from user_provide_info import main

    res = main.verify_telegram_data_json(user_input=MagicMock(), token=MagicMock())
    pass


def test_verify_telegram_data_string():
    from user_provide_info import main

    with pytest.raises(Exception):
        res = main.verify_telegram_data_string(user_input=MagicMock(), token=MagicMock())
    pass
