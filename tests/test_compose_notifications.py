from compose_notifications.main import main
from unittest.mock import MagicMock


def test_main():
    

    main(MagicMock(), 'context')
    assert True
