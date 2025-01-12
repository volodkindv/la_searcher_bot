from unittest.mock import MagicMock

from title_recognize import main


def test_get_requested_title():
    res = main.get_requested_title(request=MagicMock())
    pass


def test_main():
    res = main.main(request=MagicMock())
    pass


def test_recognize_title():
    res = main.recognize_title(line=MagicMock(), reco_type=MagicMock())
    pass


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass
