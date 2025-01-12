import importlib
import inspect
import re
from datetime import date, datetime
from pathlib import Path

import pytest


class TestSmokeTestGeneration:
    def test_generate_all(self):
        """generate all smoke testcases"""

        dir_names = [x.name for x in Path('src').glob('*')]
        dir_names.sort()
        print('')
        for dir_name in dir_names:
            if dir_name.startswith('_'):
                continue
            module = importlib.import_module(f'{dir_name}.main')
            self._generate_test_cases_for_module(
                module,
                dir_name,
                f'tests/smoke/test_{dir_name}_generated.py',
            )

    def _extract_broken_testscases(self) -> list[tuple[str, str, str]]:
        pytest_out = get_broken_testscases_text()

        res = []
        exp = re.compile('FAILED(.*)\.py::(\w*) - .*')
        for line in pytest_out.splitlines():
            if not line.strip():
                continue
            try:
                test_module_name, test_case_name = exp.findall(line)[0]
                test_module_name = test_module_name.split('/')[-1]
                res.append((test_module_name, test_case_name))
            except:
                pass
        return res

    def test_generate_signature(self):
        def example(v1: str, v2: int, v3, v4: date, v5: datetime):
            pass

        signature = self._generate_call_signature(example)
        assert signature == "v1='foo', v2=1, v3=MagicMock(), v4=date.today(), v5=datetime.now()"

    @pytest.mark.skip(reason='Использовалось для генерации тест-кейсов')
    def test_generate_cases_example(self):
        """generate testcases for single module"""
        import communicate.main

        self._generate_test_cases_for_module(communicate.main, 'communicate', 'tests/test_communicate_generated.py')

    def _generate_test_cases_for_module(self, module, module_name: str, res_filename: str) -> str:
        """generate test cases for all functions in module"""
        broken_test_cases = self._extract_broken_testscases()
        broken_test_cases_set = set(
            [f'{test_module_name}:{test_case_name}' for test_module_name, test_case_name in broken_test_cases]
        )

        template_ok = """
def test_{func_name}():
    res = main.{func_name}({args})
    pass
            
        """
        template_exception = """
def test_{func_name}():
    with pytest.raises(Exception):
        res = main.{func_name}({args})
    pass
            
        """

        ignore_list = [
            'publish_to_pubsub',
            'clean_up_content',
            'notify_admin',
            'setup_google_logging',
        ]
        # functions that already have manual testcases
        module_lines = [
            'from unittest.mock import MagicMock',
            'from datetime import date, datetime',
            'import pytest',
            f'from {module_name} import main',
        ]

        members = inspect.getmembers(module)
        for member_name, member in members:
            if member_name in ignore_list:
                continue
            if not inspect.isfunction(member):
                continue

            args_str = self._generate_call_signature(member)

            search_key = f'test_{module_name}_generated:test_{member_name}'
            template = template_ok if search_key not in broken_test_cases_set else template_exception
            testcase = template.format(module_name=module_name, func_name=member_name, args=args_str)
            module_lines.append(testcase)

        Path(res_filename).write_text('\n'.join(module_lines))
        return '\n'.join(module_lines)

    def _generate_call_signature(self, member):
        signature = inspect.signature(member)

        args = []
        for param_name in signature.parameters:
            arg_value = self._get_default_arg_value(signature.parameters[param_name])
            args.append(f'{param_name}={arg_value}')

        args_str = ', '.join(args)
        return args_str

    def _get_default_arg_value(self, param) -> str:
        if param._annotation is str:
            return "'foo'"
        elif param._annotation is int:
            return '1'
        elif param._annotation is list:
            return '[]'
        elif param._annotation is dict:
            return '{}'
        elif param._annotation is bool:
            return 'False'
        elif param._annotation is datetime:
            return 'datetime.now()'
        elif param._annotation is date:
            return 'date.today()'
        else:
            return 'MagicMock()'


def get_broken_testscases_text() -> str:
    """
    Generate smoke tests with `test_generate_all`
    run `make test`
    paste here output of pytest
    run `test_generate_all` again
    """

    return """
FAILED tests/smoke/test_api_get_active_searches_generated.py::test_evaluate_city_locations - TypeError: eval() arg 1 must be a string, bytes or code object
FAILED tests/smoke/test_api_get_active_searches_generated.py::test_time_counter_since_search_start - TypeError: '<' not supported between instances of 'MagicMock' and 'int'
FAILED tests/smoke/test_archive_to_bigquery_generated.py::test_main - ValueError: not enough values to unpack (expected 2, got 0)
FAILED tests/smoke/test_communicate_generated.py::test_api_callback_edit_inline_keyboard - TypeError: Object of type MagicMock is not JSON serializable
FAILED tests/smoke/test_communicate_generated.py::test_manage_age - AttributeError: 'NoneType' object has no attribute 'min'
FAILED tests/smoke/test_communicate_generated.py::test_manage_search_follow_mode - UnboundLocalError: local variable 'bot_message' referenced before assignment
FAILED tests/smoke/test_communicate_generated.py::test_manage_search_whiteness - UnboundLocalError: local variable 'bot_message' referenced before assignment
FAILED tests/smoke/test_communicate_generated.py::test_manage_topic_type - ValueError: The parameter `inline_keyboard` should be a sequence of sequences of InlineKeyboardButtons
FAILED tests/smoke/test_communicate_generated.py::test_process_leaving_chat_async - telegram.error.InvalidToken: The token `foo` was rejected by the server.
FAILED tests/smoke/test_communicate_generated.py::test_process_sending_message_async - telegram.error.InvalidToken: The token `foo` was rejected by the server.
FAILED tests/smoke/test_communicate_generated.py::test_process_user_coordinates - telegram.error.InvalidToken: The token `foo` was rejected by the server.
FAILED tests/smoke/test_communicate_generated.py::test_save_onboarding_step - TypeError: Object of type MagicMock is not JSON serializable
FAILED tests/smoke/test_communicate_generated.py::test_send_callback_answer_to_api - AttributeError: 'NoneType' object has no attribute 'json'
FAILED tests/smoke/test_communicate_generated.py::test_send_message_to_api - AttributeError: 'NoneType' object has no attribute 'json'
FAILED tests/smoke/test_communicate_generated.py::test_time_counter_since_search_start - TypeError: '<' not supported between instances of 'MagicMock' and 'int'
FAILED tests/smoke/test_compose_notifications_generated.py::test_check_if_need_compose_more - TypeError: Object of type MagicMock is not JSON serializable
FAILED tests/smoke/test_compose_notifications_generated.py::test_compose_com_msg_on_new_topic - TypeError: '>=' not supported between instances of 'MagicMock' and 'int'
FAILED tests/smoke/test_compose_notifications_generated.py::test_enrich_new_record_with_emoji - KeyError: <MagicMock name='mock.topic_type_id' id='138343183795200'>
FAILED tests/smoke/test_compose_notifications_generated.py::test_main - sqlalchemy.exc.ProgrammingError: (pg8000.dbapi.ProgrammingError) {'S': 'ERROR', 'V': 'ERROR', 'C': '22P02', 'M': 'inval...
FAILED tests/smoke/test_connect_to_forum_generated.py::test_get_user_attributes - requests.exceptions.MissingSchema: Invalid URL "<MagicMock name='mock.__radd__()' id='138343183880144'>": No scheme sup...
FAILED tests/smoke/test_connect_to_forum_generated.py::test_get_user_id - requests.exceptions.MissingSchema: Invalid URL "<MagicMock name='mock.__radd__()' id='138343205514752'>": No scheme sup...
FAILED tests/smoke/test_connect_to_forum_generated.py::test_main - TypeError: argument should be a bytes-like object or ASCII string, not 'MagicMock'
FAILED tests/smoke/test_connect_to_forum_generated.py::test_process_sending_message_async - telegram.error.InvalidToken: The token `foo` was rejected by the server.
FAILED tests/smoke/test_identify_updates_of_first_posts_generated.py::test_clean_up_content_2 - TypeError: expected string or bytes-like object
FAILED tests/smoke/test_identify_updates_of_first_posts_generated.py::test_compose_diff_message - TypeError: lines to compare must be str, not MagicMock (<MagicMock name='mock.__getitem__()' id='138343100205424'>)
FAILED tests/smoke/test_identify_updates_of_first_posts_generated.py::test_get_compressed_first_post - TypeError: expected string or bytes-like object
FAILED tests/smoke/test_identify_updates_of_first_posts_generated.py::test_get_field_trip_details_from_text - TypeError: expected string or bytes-like object
FAILED tests/smoke/test_identify_updates_of_first_posts_generated.py::test_get_the_list_of_coords_out_of_text - TypeError: expected string or bytes-like object
FAILED tests/smoke/test_identify_updates_of_first_posts_generated.py::test_main -   File "<string>", line 1
FAILED tests/smoke/test_identify_updates_of_first_posts_generated.py::test_process_pubsub_message -   File "<string>", line 1
FAILED tests/smoke/test_identify_updates_of_first_posts_generated.py::test_split_text_to_deleted_and_regular_parts - TypeError: expected string or bytes-like object
FAILED tests/smoke/test_identify_updates_of_folders_generated.py::test_compare_old_and_new_folder_hash_and_give_list_of_upd_folders - ValueError: malformed node or string on line <MagicMock name='mock.lineno' id='138343215306816'>: <MagicMock id='138343...
FAILED tests/smoke/test_identify_updates_of_folders_generated.py::test_main -   File "<string>", line 1
FAILED tests/smoke/test_identify_updates_of_folders_generated.py::test_process_pubsub_message -   File "<string>", line 1
FAILED tests/smoke/test_identify_updates_of_folders_generated.py::test_set_cloud_storage - ValueError: not enough values to unpack (expected 2, got 0)
FAILED tests/smoke/test_identify_updates_of_folders_generated.py::test_write_snapshot_to_cloud_storage - ValueError: not enough values to unpack (expected 2, got 0)
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_main -   File "<string>", line 1
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_parse_one_comment - TypeError: expected string or bytes-like object
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_parse_search_profile - AttributeError: 'NoneType' object has no attribute 'find'
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_process_pubsub_message -   File "<string>", line 1
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_profile_get_type_of_activity - TypeError: '>' not supported between instances of 'MagicMock' and 'int'
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_rate_limit_for_api - TypeError: '>' not supported between instances of 'MagicMock' and 'int'
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_set_cloud_storage - ValueError: not enough values to unpack (expected 2, got 0)
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_visibility_check - TypeError: expected string or bytes-like object
FAILED tests/smoke/test_identify_updates_of_topics_generated.py::test_write_snapshot_to_cloud_storage - ValueError: not enough values to unpack (expected 2, got 0)
FAILED tests/smoke/test_manage_topics_generated.py::test_process_pubsub_message -   File "<string>", line 1
FAILED tests/smoke/test_manage_users_generated.py::test_save_new_user - psycopg2.ProgrammingError: can't adapt type 'MagicMock'
FAILED tests/smoke/test_manage_users_generated.py::test_save_onboarding_step - psycopg2.ProgrammingError: can't adapt type 'MagicMock'
FAILED tests/smoke/test_manage_users_generated.py::test_save_updated_status_for_user - KeyError: <MagicMock id='138343184144592'>
FAILED tests/smoke/test_send_debug_to_admin_generated.py::test_main - TypeError: argument should be a bytes-like object or ASCII string, not 'MagicMock'
FAILED tests/smoke/test_send_debug_to_admin_generated.py::test_process_sending_message_async - telegram.error.InvalidToken: The token `123:foo` was rejected by the server.
FAILED tests/smoke/test_send_notifications_generated.py::test_finish_time_analytics - ZeroDivisionError: division by zero
FAILED tests/smoke/test_send_notifications_generated.py::test_iterate_over_notifications - TypeError: '>' not supported between instances of 'MagicMock' and 'int'
FAILED tests/smoke/test_send_notifications_generated.py::test_main - psycopg2.ProgrammingError: can't adapt type 'MagicMock'
FAILED tests/smoke/test_send_notifications_helper_2_generated.py::test_finish_time_analytics - ZeroDivisionError: division by zero
FAILED tests/smoke/test_send_notifications_helper_2_generated.py::test_main - psycopg2.ProgrammingError: can't adapt type 'MagicMock'
FAILED tests/smoke/test_send_notifications_helper_generated.py::test_finish_time_analytics - ZeroDivisionError: division by zero
FAILED tests/smoke/test_send_notifications_helper_generated.py::test_main - psycopg2.ProgrammingError: can't adapt type 'MagicMock'
FAILED tests/smoke/test_user_provide_info_generated.py::test_evaluate_city_locations - TypeError: eval() arg 1 must be a string, bytes or code object
FAILED tests/smoke/test_user_provide_info_generated.py::test_time_counter_since_search_start - TypeError: '<' not supported between instances of 'MagicMock' and 'int'
FAILED tests/smoke/test_user_provide_info_generated.py::test_verify_telegram_data_string - TypeError: object supporting the buffer API required        
"""
