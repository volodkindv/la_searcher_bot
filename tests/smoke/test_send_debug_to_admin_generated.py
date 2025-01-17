import pytest

from send_debug_to_admin import main
from tests.common import run_smoke


def test_main():
    with pytest.raises(Exception) as e:
        res = run_smoke(main.main)
    pass


def test_send_message():
    res = run_smoke(main.send_message)
    pass
