import base64
from unittest.mock import AsyncMock, patch

from telegram import Bot
from telegram.ext import ExtBot

from send_debug_to_admin import main
from tests.common import get_event_with_data, get_test_config


def test_main_positive():
    message_text = 'some text'
    event = get_event_with_data(message_text)

    with (
        patch.object(ExtBot, 'send_message') as mock_send_message,
        patch.object(Bot, 'get_me'),
    ):
        main.main(event, 'context')
        mock_send_message.assert_called_once_with(
            chat_id=get_test_config().my_telegram_id,
            text=message_text,
        )


def test_main_with_exception():
    message_text = 'some text'
    data = base64.b64encode(str({'data': {'message': message_text}}).encode())
    event = {'data': data}

    with (
        patch.object(ExtBot, 'send_message') as mock_send_message,
        patch.object(Bot, 'get_me', AsyncMock(side_effect=[Exception, None])),
    ):
        main.main(event, 'context')
        mock_send_message.assert_called_once()
        assert 'ERROR' in mock_send_message.call_args[1]['text']
