from unittest.mock import MagicMock

from check_first_posts_for_changes.main import main


def test_main():
    main(MagicMock(), 'context')
    assert True
