from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_get_requested_title():
    from title_recognize import main

    res = main.get_requested_title(request=MagicMock())
    pass


def test_main():
    from title_recognize import main

    res = main.main(request=MagicMock())
    pass


def test_recognize_title():
    from title_recognize import main

    res = main.recognize_title(line='foo', reco_type='foo')
    pass
