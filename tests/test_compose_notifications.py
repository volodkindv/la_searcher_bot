from unittest.mock import MagicMock

from compose_notifications.main import main


def test_main():
    main(MagicMock(), 'context')
    assert True
