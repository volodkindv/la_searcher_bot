import inspect
from pathlib import Path

import pytest


# @pytest.mark.skip(reason='Использовалось для генерации тест-кейсов')
class TestSmokeTestGeneration:
    def test_generate_cases(self):
        import communicate.main

        self.generate_test_cases(communicate.main, 'communicate', 'tests/test_communicate_generated.py')

    def test_generate_all_cases(self):
        dir_names = [x.name for x in Path('src').glob('*')]
        dir_names.sort()
        print('')
        for dir_name in dir_names:
            print(f'import {dir_name}.main')
            print(
                f"self.generate_test_cases( {dir_name}.main, '{dir_name}', 'tests/smoke/test_{dir_name}_generated.py')"
            )
            print('')

    def generate_test_cases(self, module, module_name: str, res_filename: str) -> str:
        template = """
def test_{func_name}():
    res = main.{func_name}({args})
    pass
            
        """

        testcases = []
        members = inspect.getmembers(module)
        for member in members:
            if not inspect.isfunction(member[1]):
                continue

            signature = inspect.signature(member[1])
            args_str = ', '.join([f'{arg}=MagicMock()' for arg in signature.parameters])

            testcase = template.format(module_name=module_name, func_name=member[0], args=args_str)
            testcases.append(testcase)

        testcases.insert(0, 'from unittest.mock import MagicMock')
        testcases.insert(0, f'from {module_name} import main')

        Path(res_filename).write_text('\n'.join(testcases))
        return '\n'.join(testcases)


    def test_gen(self):
        """copy output of test_generate_all_cases and run to generate smoke test templates"""

        import api_get_active_searches.main
        self.generate_test_cases( api_get_active_searches.main, 'api_get_active_searches', 'tests/smoke/test_api_get_active_searches_generated.py')

        import archive_notifications.main
        self.generate_test_cases( archive_notifications.main, 'archive_notifications', 'tests/smoke/test_archive_notifications_generated.py')

        import archive_to_bigquery.main
        self.generate_test_cases( archive_to_bigquery.main, 'archive_to_bigquery', 'tests/smoke/test_archive_to_bigquery_generated.py')

        import check_first_posts_for_changes.main
        self.generate_test_cases( check_first_posts_for_changes.main, 'check_first_posts_for_changes', 'tests/smoke/test_check_first_posts_for_changes_generated.py')

        import check_topics_by_upd_time.main
        self.generate_test_cases( check_topics_by_upd_time.main, 'check_topics_by_upd_time', 'tests/smoke/test_check_topics_by_upd_time_generated.py')

        import communicate.main
        self.generate_test_cases( communicate.main, 'communicate', 'tests/smoke/test_communicate_generated.py')

        import compose_notifications.main
        self.generate_test_cases( compose_notifications.main, 'compose_notifications', 'tests/smoke/test_compose_notifications_generated.py')

        import connect_to_forum.main
        self.generate_test_cases( connect_to_forum.main, 'connect_to_forum', 'tests/smoke/test_connect_to_forum_generated.py')

        import identify_updates_of_first_posts.main
        self.generate_test_cases( identify_updates_of_first_posts.main, 'identify_updates_of_first_posts', 'tests/smoke/test_identify_updates_of_first_posts_generated.py')

        import identify_updates_of_folders.main
        self.generate_test_cases( identify_updates_of_folders.main, 'identify_updates_of_folders', 'tests/smoke/test_identify_updates_of_folders_generated.py')

        import identify_updates_of_topics.main
        self.generate_test_cases( identify_updates_of_topics.main, 'identify_updates_of_topics', 'tests/smoke/test_identify_updates_of_topics_generated.py')

        import manage_topics.main
        self.generate_test_cases( manage_topics.main, 'manage_topics', 'tests/smoke/test_manage_topics_generated.py')

        import manage_users.main
        self.generate_test_cases( manage_users.main, 'manage_users', 'tests/smoke/test_manage_users_generated.py')

        import send_debug_to_admin.main
        self.generate_test_cases( send_debug_to_admin.main, 'send_debug_to_admin', 'tests/smoke/test_send_debug_to_admin_generated.py')

        import send_notifications.main
        self.generate_test_cases( send_notifications.main, 'send_notifications', 'tests/smoke/test_send_notifications_generated.py')

        import send_notifications_helper.main
        self.generate_test_cases( send_notifications_helper.main, 'send_notifications_helper', 'tests/smoke/test_send_notifications_helper_generated.py')

        import send_notifications_helper_2.main
        self.generate_test_cases( send_notifications_helper_2.main, 'send_notifications_helper_2', 'tests/smoke/test_send_notifications_helper_2_generated.py')

        import title_recognize.main
        self.generate_test_cases( title_recognize.main, 'title_recognize', 'tests/smoke/test_title_recognize_generated.py')

        import user_provide_info.main
        self.generate_test_cases( user_provide_info.main, 'user_provide_info', 'tests/smoke/test_user_provide_info_generated.py')

        import users_activate.main
        self.generate_test_cases( users_activate.main, 'users_activate', 'tests/smoke/test_users_activate_generated.py')

