from unittest.mock import MagicMock
from users_activate.main import main


def test_main():

    main(MagicMock(), 'context')
    assert True
