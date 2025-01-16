"""Parses the folder-tree on the forum, checking the last update time. Collects the list of leaf-level folders
which contain updates – and makes a pub/sub call for other script to parse content of these folders"""

import ast
import logging
from typing import Any, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup, SoupStrainer  # noqa
from google.cloud import storage

from _dependencies.commons import Topics, publish_to_pubsub, setup_google_logging
from _dependencies.misc import process_pubsub_message

setup_google_logging()


def set_cloud_storage(folder_num: str):
    """sets the basic parameters for connection to txt file in cloud storage, which stores searches snapshots"""
    bucket_name = 'bucket_for_folders_snapshots'
    blob_name = str(folder_num) + '.txt'

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    return blob


def write_snapshot_to_cloud_storage(what_to_write, folder_num):
    """writes current snapshot to txt file in cloud storage"""

    blob = set_cloud_storage(folder_num)
    blob.upload_from_string(str(what_to_write), content_type='text/plain')


def read_snapshot_from_cloud_storage(folder_num: str):
    """reads previous searches snapshot from txt file in cloud storage"""

    try:
        blob = set_cloud_storage(folder_num)
        contents_as_bytes = blob.download_as_string()
        contents = str(contents_as_bytes, 'utf-8')
        if contents == 'None':
            contents = None
    except:  # noqa
        contents = None
    return contents


def compare_old_and_new_folder_hash_and_give_list_of_upd_folders(new_str: str, old_str) -> List:
    """compare if newly parsed folder content equals the previously-saved one"""

    list_of_changed_folders = []

    # if there is no "old" version, we treat all the folder from new_str as newly parsed
    if not old_str:
        new_list = ast.literal_eval(new_str)
        for n_line in new_list:
            list_of_changed_folders.append(n_line[0])

    # if these are updates (new and old str are not equal) - combine a list of updates
    elif new_str != old_str:
        new_list = ast.literal_eval(new_str)
        old_list = ast.literal_eval(old_str)

        comparison_matrix = []

        for o_line in old_list:
            comparison_matrix.append([o_line[0], o_line[1], ''])
        for n_line in new_list:
            new_folder_trigger = True
            for m_line in comparison_matrix:
                if n_line[0] == m_line[0]:
                    new_folder_trigger = False
                    m_line[2] = n_line[1]
            if new_folder_trigger:
                comparison_matrix.append([n_line[0], '', n_line[1]])

        for line in comparison_matrix:
            if line[1] != line[2]:
                list_of_changed_folders.append(line[0])

    return list_of_changed_folders


def decompose_folder_to_subfolders_and_searches(start_folder_num) -> Tuple[List, List, List, None]:
    """Check if there are changes in folder that contain other folders"""

    page_summary_folders = []
    page_summary_searches = []
    page_full_extract_searches = []
    folder_name = None

    url = 'https://lizaalert.org/forum/viewforum.php?f=' + str(start_folder_num)

    try:
        r = requests.Session().get(url)
        only_tag = SoupStrainer('div', {'class': 'page-body'})
        soup = BeautifulSoup(r.content, features='lxml', parse_only=only_tag)
        del r  # trying to free up memory
        folder_name = soup.find('h2', {'class': 'forum-title'}).next_element.next_element
        logging.info(folder_name)

        search_code_blocks_folders = soup.find_all('div', {'class': 'forabg'})
        search_code_blocks_searches = soup.find_all('div', {'class': 'forumbg'})
        del soup  # trying to free up memory

    except Exception as e1:
        logging.info(f'Request to forum was unsuccessful for url {url}')
        logging.exception(e1)
        search_code_blocks_folders = None
        search_code_blocks_searches = None

    try:
        if search_code_blocks_folders:
            for block in search_code_blocks_folders:
                folders = block.find_all('li', {'class': 'row'})
                for folder in folders:
                    # found no cases where there can be more than 1 topic name or date, so find i/o find_all is used
                    folder_num_str = folder.find('a', {'class': 'forumtitle'})['href']

                    start_symb_to_del = folder_num_str.find('&sid=')
                    if start_symb_to_del != -1:
                        folder_num = int(folder_num_str[18:start_symb_to_del])
                    else:
                        folder_num = int(folder_num_str[18:])

                    try:
                        folder_time_str = folder.find('time')['datetime']
                    except:  # noqa
                        folder_time_str = None

                    # remove useless folders: Справочники, Снаряжение, Постскриптум and all from Обучение и Тренировки
                    # NB! there was an idea to remove this part of code and make a limitation basing on info in PSQL.
                    # However, in reality, this script does not import any SQL capabilities. Thus, it's more
                    # efficient from cold-start perspective / time for script initiation & memory it occupies – not to
                    # use SQL call here as well. So the limitation is made on python level.
                    if folder_num not in {84, 113, 112, 270, 86, 87, 88, 165, 365, 89, 172, 91, 90, 316, 234, 230, 319}:
                        page_summary_folders.append([folder_num, folder_time_str])

    except Exception as e2:
        logging.info(f'Folder code blocks identification was not successful, fired an error for {start_folder_num}')
        logging.exception(e2)

    try:
        if search_code_blocks_searches:
            for block in search_code_blocks_searches:
                searches = block.find_all('dl', 'row-item')  # memo: w/o "class:row-item" - to catch diff "row-items"

                for i in range(len(searches) - 1):
                    page_full_extract_searches.append(str(searches[i + 1]))

                    # only title + time of the last reply
                    search_title_block = searches[i + 1].find('a', 'topictitle')
                    search_title = search_title_block.next_element

                    try:
                        search_time_str = searches[i + 1].find('time')['datetime']
                    except:  # noqa
                        search_time_str = None

                    page_summary_searches.append([search_title, search_time_str])

    except Exception as e3:
        logging.info(f'Searches code blocks identification was not successful, fired an error for {start_folder_num}')
        logging.exception(e3)

    logging.info(f'Page summary searches: {str(page_summary_searches)}')

    return page_summary_folders, page_summary_searches, page_full_extract_searches, folder_name


class FolderForDecompose:
    def __init__(
        self,
        mother_folder_num=None,
        mother_folder_name=None,
        old_child_folders_str=None,
        old_child_searches_str=None,
        new_child_folders_str=None,
        new_child_searches_str=None,
        decomposition_status=None,
        mother_file_folders=None,
        mother_file_searches=None,
        searches_extract=None,
    ):
        self.mother_folder_num = mother_folder_num
        self.mother_folder_name = mother_folder_name
        self.old_child_folders_str = old_child_folders_str
        self.old_child_searches_str = old_child_searches_str
        self.new_child_folders_str = new_child_folders_str
        self.new_child_searches_str = new_child_searches_str
        self.decomposition_status = decomposition_status
        self.mother_file_folders = mother_file_folders
        self.mother_file_searches = mother_file_searches
        self.searches_extract = searches_extract

    def __str__(self):
        return str(
            [
                self.mother_folder_num,
                self.old_child_searches_str,
                self.new_child_searches_str,
                self.old_child_folders_str,
                self.new_child_folders_str,
                self.decomposition_status,
                self.mother_file_folders,
                self.mother_file_searches,
            ]
        )


def main(event, context):  # noqa
    """main function"""

    list_of_updates = []
    list_of_updated_low_level_folders = []

    # check the initial 000 folder: what pub/sub sent & what is in storage

    folder_root = FolderForDecompose()
    folder_root.mother_folder_num = '000'

    list_of_updates.append(folder_root)

    for folder in list_of_updates:
        # if folder was not decomposed yet - we need to do it (if was, we're just skipping it)
        if not folder.decomposition_status:
            folder.mother_file_folders = str(folder.mother_folder_num) + '_folders'
            folder.mother_file_searches = str(folder.mother_folder_num) + '_searches'
            folder.old_child_folders_str = read_snapshot_from_cloud_storage(folder.mother_file_folders)
            folder.old_child_searches_str = read_snapshot_from_cloud_storage(folder.mother_file_searches)

            if folder.mother_folder_num == '000':
                folder.new_child_folders_str = process_pubsub_message(event)
                folder.new_child_searches_str = None
            else:
                (
                    list_of_decomposed_folders,
                    list_of_decomposed_searches,
                    list_of_searches_details,
                    mother_folder_name,
                ) = decompose_folder_to_subfolders_and_searches(folder.mother_folder_num)
                folder.new_child_folders_str = str(list_of_decomposed_folders)
                folder.new_child_searches_str = str(list_of_decomposed_searches)
                folder.searches_extract = str(list_of_searches_details)
                folder.mother_folder_name = mother_folder_name

            list_of_new_folders = compare_old_and_new_folder_hash_and_give_list_of_upd_folders(
                folder.new_child_folders_str, folder.old_child_folders_str
            )

            logging.info(f'List of new folders in {str(folder.mother_folder_num)}: {str(list_of_new_folders)}')

            for line in list_of_new_folders:
                child_folder = FolderForDecompose()
                child_folder.mother_folder_num = str(line)
                list_of_updates.append(child_folder)

            folder.decomposition_status = 'decomposed'
            write_snapshot_to_cloud_storage(folder.new_child_folders_str, folder.mother_file_folders)
            write_snapshot_to_cloud_storage(folder.new_child_searches_str, folder.mother_file_searches)

    for line in list_of_updates:
        if line.new_child_searches_str != line.old_child_searches_str:
            list_of_updated_low_level_folders.append([line.mother_folder_num, line.mother_folder_name])

    logging.info('The below list is to be sent to "Identify updates of topics" script via pub/sub')
    for line in list_of_updated_low_level_folders:
        logging.info(line)

    if list_of_updated_low_level_folders:
        publish_to_pubsub(Topics.topic_to_run_parsing_script, str(list_of_updated_low_level_folders))

    return None
