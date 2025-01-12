from datetime import date, datetime
from unittest.mock import MagicMock

import pytest


def test_check_updates_in_folder_with_folders():
    from check_topics_by_upd_time import main

    res = main.check_updates_in_folder_with_folders(requests_session=MagicMock(), start_folder_num=MagicMock())
    pass


def test_get_the_list_folders_to_update():
    from check_topics_by_upd_time import main

    res = main.get_the_list_folders_to_update(
        list_of_folders_and_times=MagicMock(), now_time=MagicMock(), delay_time=MagicMock()
    )
    pass


def test_main():
    from check_topics_by_upd_time import main

    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_time_delta():
    from check_topics_by_upd_time import main

    res = main.time_delta(now=MagicMock(), time=MagicMock())
    pass
