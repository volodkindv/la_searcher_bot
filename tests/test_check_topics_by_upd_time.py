from check_topics_by_upd_time.main import main
from unittest.mock import MagicMock


def test_main():
    
    main(MagicMock(), 'context')
    assert True
