from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from _dependencies import misc
from _dependencies.misc import age_writer, time_counter_since_search_start
from tests.common import get_test_config


def test_notify_admin(patch_pubsub_client, bot_mock_send_message: AsyncMock):
    data = 'some message'

    misc.notify_admin(data)
    bot_mock_send_message.assert_called_once_with(chat_id=get_test_config().my_telegram_id, text=data)


def test_make_api_call():
    # TODO mock requests
    misc.make_api_call('test', {'a: 1'})


@pytest.mark.parametrize(
    'minutes_ago,hours_ago,days_ago,result',
    [
        (0, 0, 0, ['Начинаем искать', 0]),
        (0, 1, 0, ['1 час', 0]),
        (0, 10, 0, ['10 часов', 0]),
        (0, 0, 2, ['2 дня', 2]),
    ],
)
def test_time_counter_since_search_start(minutes_ago: int, hours_ago: int, days_ago: int, result: str):
    start_datetime = datetime.now() - timedelta(minutes=minutes_ago, hours=hours_ago, days=days_ago)
    res = time_counter_since_search_start(start_datetime)
    assert res == result


@pytest.mark.parametrize(
    'age,result',
    [
        (0, ''),
        (1, '1 год'),
        (5, '5 лет'),
        (22, '22 года'),
    ],
)
def test_age_writer(age: int, result: str):
    assert result == age_writer(age)
