from unittest.mock import MagicMock

from communicate.main import main


def test_update_and_download_list_of_regions():
    main(MagicMock())
