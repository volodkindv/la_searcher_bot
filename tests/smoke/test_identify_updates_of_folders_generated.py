from datetime import date, datetime
from unittest.mock import MagicMock

from identify_updates_of_folders import main


def test_compare_old_and_new_folder_hash_and_give_list_of_upd_folders():
    res = main.compare_old_and_new_folder_hash_and_give_list_of_upd_folders(new_str=MagicMock(), old_str=MagicMock())
    pass


def test_decompose_folder_to_subfolders_and_searches():
    res = main.decompose_folder_to_subfolders_and_searches(start_folder_num=MagicMock())
    pass


def test_main():
    res = main.main(event=MagicMock(), context=MagicMock())
    pass


def test_process_pubsub_message():
    res = main.process_pubsub_message(event={})
    pass


def test_read_snapshot_from_cloud_storage():
    res = main.read_snapshot_from_cloud_storage(folder_num=MagicMock())
    pass


def test_set_cloud_storage():
    res = main.set_cloud_storage(folder_num=MagicMock())
    pass


def test_setup_google_logging():
    res = main.setup_google_logging()
    pass


def test_write_snapshot_to_cloud_storage():
    res = main.write_snapshot_to_cloud_storage(what_to_write=MagicMock(), folder_num=MagicMock())
    pass
