import importlib
import inspect
import re
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path

import pytest


class TestSmokeTestGeneration:
    @pytest.mark.skip(reason='Использовалось для генерации тест-кейсов')
    def test_generate_all(self):
        """
        Generate all smoke testcases
        TODO move to separate script, not test
        """

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

    @lru_cache
    def _extract_broken_testscases(self) -> list[tuple[str, str, str]]:
        pytest_out = get_broken_testscases_text()

        res = []
        exp = re.compile('FAILED(.*)\.py::(\w*)( .*)*$')
        for line in pytest_out.splitlines():
            if not line.strip().startswith('FAILED'):
                continue
            try:
                test_module_name, test_case_name, tail_ = exp.findall(line)[0]
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
    from {module_name} import main
    res = main.{func_name}({args})
    pass
            
        """
        template_exception = """
def test_{func_name}():
    from {module_name} import main
    with pytest.raises(Exception):
        res = main.{func_name}({args})
    pass
            
        """

        ignore_list = [
            # 'publish_to_pubsub',
            # 'clean_up_content',
            # 'notify_admin',
            # 'setup_google_logging',
        ]
        # functions that already have manual testcases
        module_lines = [
            'from unittest.mock import MagicMock',
            'from datetime import date, datetime',
            'import pytest',
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
    Clear file `build/pytest.log`
    Generate smoke tests with `test_generate_all`
    mark skip test `test_generate_all`
    run `make test -> build/pytest.log`
    run `test_generate_all` again
    """
    from pathlib import Path

    return Path('build/pytest.log').read_text()
