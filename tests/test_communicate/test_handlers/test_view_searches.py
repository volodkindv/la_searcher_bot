import datetime
from unittest.mock import MagicMock

import pytest
import sqlalchemy

from communicate import main
from communicate._utils.common import UserInputState
from communicate._utils.database import DBClient
from communicate._utils.handler_context import TGHandlerContext
from communicate._utils.handlers import view_searches_handlers
from tests.common import fake
from tests.factories import db_factories


@pytest.fixture
def region_id(session):
    _region_id = fake.pyint(min_value=1_000_000_000, max_value=2_000_000_000)
    yield _region_id
    session.execute(
        sqlalchemy.text('DELETE FROM searches WHERE forum_folder_id = :region_id'),
        {'region_id': _region_id},
    )
    session.commit()


def test__compose_text_message_of_all_searches(db_client: DBClient, user_id: int, region_id: int):
    count = 3
    searches = db_factories.SearchFactory.create_batch_sync(
        count,
        forum_folder_id=region_id,
        search_start_time=datetime.datetime.now(),
        status='Ищем',
    )
    for search in searches:
        db_factories.SearchHealthCheckFactory.create_sync(search_forum_num=search.search_forum_num, status='ok')

    message = view_searches_handlers._compose_text_message_of_all_searches(db_client, region_id, 'name of region')

    lines = message.splitlines()
    assert len(lines) == count + 1
    for search in searches:
        assert search.display_name in message


def test__compose_text_message_on_active_searches(db_client: DBClient, user_id: int, region_id: int):
    count = 3
    searches = db_factories.SearchFactory.create_batch_sync(
        count,
        forum_folder_id=region_id,
        search_start_time=datetime.datetime.now(),
        status='Ищем',
    )
    for search in searches:
        db_factories.SearchHealthCheckFactory.create_sync(search_forum_num=search.search_forum_num, status='ok')

    message = view_searches_handlers._compose_text_message_on_active_searches(
        db_client, region_id, 'name of region', user_id
    )

    lines = message.splitlines()
    assert len(lines) == count + 1
    for search in searches:
        assert search.display_name in message


def test__compose_ikb_of_last_searches(db_client: DBClient, user_id: int, region_id: int):
    count = 3
    searches = db_factories.SearchFactory.create_batch_sync(
        count,
        forum_folder_id=region_id,
        search_start_time=datetime.datetime.now(),
        status='Ищем',
    )
    for search in searches:
        db_factories.SearchHealthCheckFactory.create_sync(search_forum_num=search.search_forum_num, status='ok')

    ikb_data = view_searches_handlers._compose_ikb_of_last_searches(
        db_client, user_id, region_id, 'name of region', False
    )

    assert len(ikb_data.rows) == count


def test__compose_ikb_of_active_searches(db_client: DBClient, user_id: int, region_id: int):
    count = 3
    searches = db_factories.SearchFactory.create_batch_sync(
        count,
        forum_folder_id=region_id,
        search_start_time=datetime.datetime.now(),
        status='Ищем',
    )
    for search in searches:
        db_factories.SearchHealthCheckFactory.create_sync(search_forum_num=search.search_forum_num, status='ok')

    ikb_data = view_searches_handlers._compose_ikb_of_active_searches(db_client, user_id, region_id, 'name of region')

    assert len(ikb_data.rows) == count


# ═══════════════════════════════════════════════════════════════════════
# Regression: text command «посмотреть актуальные поиски» must consume the
# context so the dispatcher does NOT fall through to the «не понимаю такой
# команды» fallback. The handler sends its replies via ctx.send_message() /
# ctx.tg_api.send_message(), which do NOT mark the context as consumed — the
# fix is an explicit ctx.mark_consumed() at the end of handle_view_searches.
# ═══════════════════════════════════════════════════════════════════════


def _make_update_params(text: str = 'посмотреть актуальные поиски') -> MagicMock:
    update_params = MagicMock()
    update_params.got_message = text
    update_params.got_callback = None
    update_params.user_latitude = None
    update_params.user_longitude = None
    update_params.user_id = 12345
    update_params.callback_query_id = None
    update_params.callback_query = None
    return update_params


def _make_db_mock() -> MagicMock:
    db_mock = MagicMock()
    db_mock.get_user_input_state.return_value = UserInputState.not_defined
    db_mock.get_search_follow_mode.return_value = False
    db_mock.is_user_tester.return_value = False
    db_mock.get_user_reg_folders_preferences.return_value = [1]
    db_mock.get_geo_folders_db.return_value = [(1, 'Москва')]
    db_mock.get_user_coordinates_or_none.return_value = (None, None)
    db_mock.get_active_searches_in_one_region.return_value = []
    db_mock.get_active_searches_in_region_limit_20.return_value = []
    db_mock.get_all_last_searches_in_region_limit_20.return_value = []
    db_mock.get_folders_with_followed_searches.return_value = []
    return db_mock


def test_handle_view_searches_marks_context_consumed():
    """«посмотреть актуальные поиски» must be recognized as consumed.

    Without ctx.mark_consumed() the dispatcher treats the handler as not
    fired (send_message does not consume) and replies «не понимаю такой
    команды» right after the searches list.
    """
    ctx = TGHandlerContext(
        update_params=_make_update_params(),
        extra_params=MagicMock(),
        db=_make_db_mock(),
        tg_api=MagicMock(),
    )

    consumed = main._run_registered_handlers(ctx, text='посмотреть актуальные поиски')

    assert consumed is True
    assert ctx.is_consumed


def test_view_searches_text_does_not_trigger_unknown_command_fallback(monkeypatch):
    """Full handler chain: searches list is sent, «не понимаю такой команды» is NOT."""
    db_mock = _make_db_mock()
    tg_api_mock = MagicMock()

    monkeypatch.setattr('communicate.main.db', lambda: db_mock)
    monkeypatch.setattr('communicate.main.tg_api', lambda: tg_api_mock)

    extra_params = MagicMock()
    extra_params.user_input_state = UserInputState.not_defined

    main._run_handlers(_make_update_params(), extra_params)

    sent_messages = [call.args[1].text for call in tg_api_mock.send_message.call_args_list]
    assert sent_messages, 'список поисков должен быть отправлен'
    assert all('не понимаю такой команды' not in message for message in sent_messages)


@pytest.mark.parametrize(
    'raw_text',
    [
        'ПОСМОТРЕТЬ АКТУАЛЬНЫЕ ПОИСКИ',
        '/View_Act_Searches',
        '  /view_act_searches  ',
        'Посмотреть Последние Поиски',
    ],
)
def test_handle_view_searches_case_insensitive_lookup(raw_text: str):
    """Commands in any case must not crash with KeyError.

    The dispatcher matches handlers on lowercased text, but the handler used
    to look up the search-list type with the RAW got_message — a user typing
    "/VIEW_ACT_SEARCHES" or capitalizing the phrase would get KeyError,
    the handler would crash and the dispatcher would fall through to
    «не понимаю такой команды». The lookup key must be normalized.
    """
    ctx = TGHandlerContext(
        update_params=_make_update_params(text=raw_text),
        extra_params=MagicMock(),
        db=_make_db_mock(),
        tg_api=MagicMock(),
    )

    consumed = main._run_registered_handlers(ctx, text=raw_text.strip().lower())

    assert consumed is True
    assert ctx.is_consumed
