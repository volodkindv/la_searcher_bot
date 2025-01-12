import inspect
from pathlib import Path

import pytest


class TestSmokeTestGeneration:
    def test_generate_all(self):
        """generate all smoke testcases"""
        import importlib

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

    def test_generate_signature(self):
        def example(v1: str, v2: int, v3=None):
            pass

        signature = self._generate_call_signature(example)
        assert signature == "v1='foo', v2=1, v3=MagicMock(v3=None)"

    @pytest.mark.skip(reason='Использовалось для генерации тест-кейсов')
    def test_generate_cases_example(self):
        """generate testcases for single module"""
        import communicate.main

        self._generate_test_cases_for_module(communicate.main, 'communicate', 'tests/test_communicate_generated.py')

    def _generate_test_cases_for_module(self, module, module_name: str, res_filename: str) -> str:
        """generate test cases for all functions in module"""
        template = """
def test_{func_name}():
    res = main.{func_name}({args})
    pass
            
        """

        ignore_list = [
            'publish_to_pubsub',
            'clean_up_content',
            'notify_admin',
        ]
        # functions that already have manual testcases
        testcases = []
        members = inspect.getmembers(module)
        for member_name, member in members:
            if member_name in ignore_list:
                continue
            if not inspect.isfunction(member):
                continue

            args_str = self._generate_call_signature(member)

            testcase = template.format(module_name=module_name, func_name=member_name, args=args_str)
            testcases.append(testcase)

        testcases.insert(0, 'from unittest.mock import MagicMock')
        testcases.insert(0, f'from {module_name} import main')

        Path(res_filename).write_text('\n'.join(testcases))
        return '\n'.join(testcases)

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
        else:
            return 'MagicMock()'
