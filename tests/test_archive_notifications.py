from unittest.mock import MagicMock
from archive_notifications.main import main


def test_main():
    
    main(MagicMock(), 'context')
    assert True
