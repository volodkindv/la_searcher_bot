from unittest.mock import MagicMock

from check_topics_by_upd_time.main import main


def test_main():
    main(MagicMock(), 'context')
    assert True
