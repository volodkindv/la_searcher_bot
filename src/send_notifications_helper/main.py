"""Send the prepared notifications to users (text and location) via Telegram"""

import ast
import datetime
import json
import logging
import time
import urllib.request
from typing import Any, List, Optional

import requests
from psycopg2.extensions import cursor

from _dependencies.commons import (
    Topics,
    get_app_config,
    publish_to_pubsub,
    setup_google_logging,
    sql_connect_by_psycopg2,
)
from _dependencies.misc import (
    generate_random_function_id,
    get_change_log_update_time,
    notify_admin,
    process_pubsub_message_v2,
    save_sending_status_to_notif_by_user,
    send_location_to_api,
)

setup_google_logging()

# To get rid of telegram "Retrying" Warning logs, which are shown in GCP Log Explorer as Errors.
# Important – these are not errors, but just informational warnings that there were retries, that's why we exclude them
logging.getLogger('telegram.vendor.ptb_urllib3.urllib3').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

SCRIPT_SOFT_TIMEOUT_SECONDS = 55  # after which iterations should stop to prevent the whole script timeout
OFFSET_VS_INITIAL_FUNCTION = 800
INTERVAL_TO_CHECK_PARALLEL_FUNCTION_SECONDS = 70  # window within which we check for started parallel function
SLEEP_TIME_FOR_NEW_NOTIFS_RECHECK_SECONDS = 0

analytics_notif_times = []
analytics_delays = []
analytics_parsed_times = []


def send_message_to_api(session, bot_token, user_id, message, params):
    """send message directly to Telegram API w/o any wrappers ar libraries"""

    try:
        parse_mode = ''
        disable_web_page_preview = ''
        reply_markup = ''
        if params:
            if 'parse_mode' in params.keys():
                parse_mode = f'&parse_mode={params["parse_mode"]}'
            if 'disable_web_page_preview' in params.keys():
                disable_web_page_preview = f'&disable_web_page_preview={params["disable_web_page_preview"]}'
            if 'reply_markup' in params.keys():
                reply_markup_temp = params['reply_markup']
                reply_markup_json = json.dumps(reply_markup_temp)
                reply_markup_string = str(reply_markup_json)
                reply_markup_encoded = urllib.parse.quote(reply_markup_string)
                reply_markup = f'&reply_markup={reply_markup_encoded}'

                logging.info(f'{reply_markup_temp=}')
                logging.info(f'{reply_markup_json=}')
                logging.info(f'{reply_markup_string=}')
                logging.info(f'{reply_markup_encoded=}')
                logging.info(f'{reply_markup=}')

        message_encoded = urllib.parse.quote(message)

        request_text = (
            f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={user_id}'
            f'{parse_mode}{disable_web_page_preview}{reply_markup}&text={message_encoded}'
        )

        r = session.get(request_text)

    except Exception as e:
        logging.exception(e)
        logging.info('Error in getting response from Telegram')
        r = None

    return r


def check_first_notif_to_send(cur: cursor):
    """return a first message_id for function to start sending"""

    sql_text_psy = f"""
                    WITH notification AS (
                    SELECT
                        message_id,
                        message_type,
                        (CASE
                            WHEN DENSE_RANK() OVER (
                                PARTITION BY change_log_id, user_id, message_type ORDER BY mailing_id) +
                                DENSE_RANK() OVER (
                                PARTITION BY change_log_id, user_id, message_type ORDER BY mailing_id DESC)
                                -1 = 1
                            THEN 'no_doubling'
                            ELSE 'doubling'
                        END) AS doubling
                    FROM
                        notif_by_user
                    WHERE
                        completed IS NULL AND
                        cancelled IS NULL
                    ORDER BY 1
                    LIMIT 1
                    OFFSET {OFFSET_VS_INITIAL_FUNCTION})

                    SELECT * FROM notification WHERE doubling = 'no_doubling'
                    /*action='check_first_notif_to_send_helper' */;
                    """

    cur.execute(sql_text_psy)
    notification = cur.fetchone()

    if not notification:
        return None

    try:
        message_id, message_type, doubling = notification
        if message_type == 'coords':
            message_id += 1

    except Exception as e:
        logging.exception(e)
        message_id = None

    return message_id


def check_for_notifs_to_send(cur, first_message):
    """return a notification which should be sent"""

    # TODO: can "doubling" calculation be done not dynamically but as a field of table?
    sql_text_psy = f"""
                    WITH notification AS (
                    SELECT
                        message_id,
                        user_id,
                        created,
                        completed,
                        cancelled,
                        message_content,
                        message_type,
                        message_params,
                        message_group_id,
                        change_log_id,
                        mailing_id,
                        (CASE
                            WHEN DENSE_RANK() OVER (
                                PARTITION BY change_log_id, user_id, message_type ORDER BY mailing_id) +
                                DENSE_RANK() OVER (
                                PARTITION BY change_log_id, user_id, message_type ORDER BY mailing_id DESC)
                                -1 = 1
                            THEN 'no_doubling'
                            ELSE 'doubling'
                        END) AS doubling,
                        failed
                    FROM
                        notif_by_user
                    WHERE
                        completed IS NULL AND
                        cancelled IS NULL AND
                        message_id >= {first_message}
                    ORDER BY 1
                    LIMIT 1)

                    SELECT
                        n.*,
                        s.status AS status,
                        cl.change_type
                    FROM
                        notification AS n
                    LEFT JOIN
                        change_log AS cl
                    ON
                        n.change_log_id=cl.id
                    LEFT JOIN
                        searches AS s
                    ON
                        cl.search_forum_num = s.search_forum_num

                    /*action='check_for_notifs_to_send_helper' */
                    ;
                    """

    cur.execute(sql_text_psy)
    notification = cur.fetchone()

    return notification


def process_response(user_id, response):
    """process response received as a result of Telegram API call while sending message/location"""

    try:
        if response.ok:
            logging.info(f'message to {user_id} was successfully sent')
            return 'completed'

        elif response.status_code == 400:  # Bad Request
            logging.info(f'Bad Request: message to {user_id} was not sent, {response.reason=}')
            logging.exception('BAD REQUEST')
            return 'cancelled_bad_request'

        elif response.status_code == 403:  # FORBIDDEN
            logging.info(f'Forbidden: message to {user_id} was not sent, {response.reason=}')
            action = None
            if response.text.find('bot was blocked by the user') != -1:
                action = 'block_user'
            if response.text.find('user is deactivated') != -1:
                action = 'delete_user'
            if action:
                message_for_pubsub = {'action': action, 'info': {'user': user_id}}
                publish_to_pubsub(Topics.topic_for_user_management, message_for_pubsub)
                logging.info(f'Identified user id {user_id} to do {action}')
            return 'cancelled'

        elif 420 <= response.status_code <= 429:  # 'Flood Control':
            logging.info(f'Flood Control: message to {user_id} was not sent, {response.reason=}')
            logging.exception('FLOOD CONTROL')
            time.sleep(5)  # to mitigate flood control
            return 'failed_flood_control'

        else:
            logging.info(f'UNKNOWN ERROR: message to {user_id} was not sent, {response.reason=}')
            logging.exception('UNKNOWN ERROR')
            return 'cancelled'

    except Exception as e:
        logging.info('Response is corrupted')
        logging.exception(e)
        return 'failed'


def send_single_message(bot_token, user_id, message_content, message_params, message_type, admin_id, session):
    """send one message to telegram"""

    if message_params:
        # convert string to bool
        if 'disable_web_page_preview' in message_params:
            message_params['disable_web_page_preview'] = message_params['disable_web_page_preview'] == 'True'

    try:
        response = None
        if message_type == 'text':
            response = send_message_to_api(session, bot_token, user_id, message_content, message_params)

        elif message_type == 'coords':
            response = send_location_to_api(session, bot_token, user_id, message_params)

        result = process_response(user_id, response)

    except Exception as e:  # when sending to telegram fails by other reasons
        error_description = str(e)

        # if user blocked the bot OR user is deactivated (deleted telegram account)
        if (
            error_description.find('bot was blocked by the user') != -1
            or error_description.find('user is deactivated') != -1
        ):
            if error_description.find('bot was blocked by the user') != -1:
                action = 'block_user'
            else:
                action = 'delete_user'
            message_for_pubsub = {'action': action, 'info': {'user': user_id}}
            publish_to_pubsub(Topics.topic_for_user_management, message_for_pubsub)

            logging.info(f'Identified user id {user_id} to do {action}')
            result = 'cancelled'

        else:
            result = 'failed'

            logging.info(f'failed sending to telegram user={user_id}, message={message_content}')
            logging.exception(error_description)

    return result


def iterate_over_notifications(
    bot_token: str, admin_id: str, script_start_time: datetime.datetime, session: requests.Session, function_id: int
) -> List:
    """iterate over all available notifications, finishes if timeout is met or no new notifications"""

    set_of_change_ids = set()

    with sql_connect_by_psycopg2() as conn_psy, conn_psy.cursor() as cur:
        trigger_to_continue_iterations = True

        message_id_of_first_message = check_first_notif_to_send(cur)
        if not message_id_of_first_message:
            trigger_to_continue_iterations = False

        while trigger_to_continue_iterations:
            # analytics on sending speed - start for every user/notification
            analytics_sm_start = datetime.datetime.now()
            analytics_iteration_start = datetime.datetime.now()
            analytics_sql_start = datetime.datetime.now()

            # check if there are any non-notified users
            message_to_send = check_for_notifs_to_send(cur, message_id_of_first_message)

            analytics_sql_finish = datetime.datetime.now()
            analytics_sql_duration = round((analytics_sql_finish - analytics_sql_start).total_seconds(), 2)

            logging.info('time: -------------- loop start -------------')
            logging.info(f'{message_to_send}')
            logging.info(f'time: {analytics_sql_duration:.2f} – reading sql')

            if message_to_send:
                doubling_trigger = message_to_send[11]
                message_id = message_to_send[0]
                change_log_id = message_to_send[9]
                change_log_upd_time = get_change_log_update_time(cur, change_log_id)

                if doubling_trigger == 'no_doubling':
                    user_id = message_to_send[1]
                    message_type = message_to_send[6]
                    message_params = ast.literal_eval(message_to_send[7]) if message_to_send[7] else {}

                    message_content = message_to_send[5]
                    # limitation to avoid telegram "message too long"
                    if message_content and len(message_content) > 3000:
                        message_content = f'{message_content[:1500]}...{message_content[-1000:]}'

                    analytics_pre_sending_msg = datetime.datetime.now()

                    status = message_to_send[13]
                    change_type = message_to_send[14]

                    # if notif is about field trips or coords change and search is inactive – no need to send it
                    if change_type in {5, 6, 7, 8} and status != 'Ищем':
                        result = 'cancelled'
                    else:
                        result = send_single_message(
                            bot_token, user_id, message_content, message_params, message_type, admin_id, session
                        )

                    analytics_send_finish = datetime.datetime.now()
                    analytics_send_start_finish = round(
                        (analytics_send_finish - analytics_pre_sending_msg).total_seconds(), 2
                    )
                    logging.info(f'time: {analytics_send_start_finish:.2f} – sending msg')

                else:
                    result = 'cancelled_due_to_doubling'
                    notify_admin('cancelled_due_to_doubling!')
                    analytics_pre_sending_msg = datetime.datetime.now()

                analytics_save_sql_start = datetime.datetime.now()

                # save result of sending telegram notification into SQL notif_by_user
                save_sending_status_to_notif_by_user(cur, message_id, result)

                # save metric: how long does it took from creation to completion
                if result == 'completed':
                    creation_time = message_to_send[2]

                    set_of_change_ids.add(change_log_id)

                    completion_time = datetime.datetime.now()
                    duration_complete_vs_create_minutes = round(
                        (completion_time - creation_time).total_seconds() / 60, 2
                    )
                    logging.info(f'metric: creation to completion time – {duration_complete_vs_create_minutes} min')
                    analytics_delays.append(duration_complete_vs_create_minutes)

                    duration_complete_vs_parsed_time_minutes = round(
                        (completion_time - change_log_upd_time).total_seconds() / 60, 2
                    )
                    logging.info(f'metric: parsing to completion time – {duration_complete_vs_parsed_time_minutes} min')
                    analytics_parsed_times.append(duration_complete_vs_parsed_time_minutes)

                analytics_after_double_saved_in_sql = datetime.datetime.now()
                analytics_save_sql_duration = round(
                    (analytics_after_double_saved_in_sql - analytics_save_sql_start).total_seconds(), 2
                )
                logging.info(f'time: {analytics_save_sql_duration:.2f} – saving to sql')

                analytics_doubling_checked_saved_to_sql = round(
                    (analytics_after_double_saved_in_sql - analytics_pre_sending_msg).total_seconds(), 2
                )
                logging.info(f'time: {analytics_doubling_checked_saved_to_sql:.2f} – check -> save to sql')

                # analytics on sending speed - finish for every user/notification
                analytics_sm_finish = datetime.datetime.now()
                analytics_sm_duration = (analytics_sm_finish - analytics_sm_start).total_seconds()
                analytics_notif_times.append(analytics_sm_duration)

                no_new_notifications = False

            else:
                # wait for some time – maybe any new notification will pop up
                time.sleep(SLEEP_TIME_FOR_NEW_NOTIFS_RECHECK_SECONDS)

                message_to_send = check_for_notifs_to_send(cur, message_id_of_first_message)

                no_new_notifications = False if message_to_send else True

            # check if not too much time passed (not more than 500 seconds)
            now = datetime.datetime.now()

            if (now - script_start_time).total_seconds() > SCRIPT_SOFT_TIMEOUT_SECONDS:
                timeout = True
            else:
                timeout = False

            # final decision if while loop should be continued
            if not no_new_notifications and not timeout:
                trigger_to_continue_iterations = True
            else:
                trigger_to_continue_iterations = False

            """if not no_new_notifications and timeout:
                message_for_pubsub = {'triggered_by_func_id': function_id, 'text': 'next iteration'}
                publish_to_pubsub(Topics.topic_to_send_notifications, message_for_pubsub)"""

            analytics_end_of_iteration = datetime.datetime.now()
            analytics_iteration_duration = round(
                (analytics_end_of_iteration - analytics_iteration_start).total_seconds(), 2
            )
            logging.info(f'time: {analytics_iteration_duration:.2f} – iteration duration')

        cur.close()
    conn_psy.close()

    list_of_change_ids = list(set_of_change_ids)

    return list_of_change_ids


def check_and_save_event_id(
    context: str, event: str, function_id: int, changed_ids: Optional[List], triggered_by_func_id
) -> bool:
    """Work with PSQL table functions_registry. Goal of the table & function is to avoid parallel work of
    two send_notifications_helper functions."""

    def check_if_other_functions_are_working():
        """Check in PSQL in there's the same function 'send_notifications_helper' working in parallel"""

        conn_psy = sql_connect_by_psycopg2()
        cur = conn_psy.cursor()

        sql_text_psy = f"""
                        SELECT
                            event_id
                        FROM
                            functions_registry
                        WHERE
                            time_start > NOW() - interval '{INTERVAL_TO_CHECK_PARALLEL_FUNCTION_SECONDS} seconds' AND
                            time_finish IS NULL AND
                            cloud_function_name  = 'send_notifications_helper'
                        ;
                        /*action='check_if_there_is_parallel_notif_function' */
                        ;"""

        cur.execute(sql_text_psy)
        lines = cur.fetchone()

        parallel_functions = True if lines else False

        cur.close()
        conn_psy.close()

        return parallel_functions

    def record_start_of_function(event_num: int, function_num: int, triggered_by_func_num: int) -> None:
        """Record into PSQL that this function started working (id = id of the respective pub/sub event)"""

        conn_psy = sql_connect_by_psycopg2()
        cur = conn_psy.cursor()

        sql_text_psy = """
                        INSERT INTO
                            functions_registry
                        (event_id, time_start, cloud_function_name, function_id, triggered_by_func_id)
                        VALUES
                        (%s, %s, %s, %s, %s);
                        /*action='save_start_of_notif_helper_function' */
                        ;"""

        cur.execute(
            sql_text_psy,
            (event_num, datetime.datetime.now(), 'send_notifications_helper', function_num, triggered_by_func_num),
        )
        logging.info(f'function was triggered by event {event_num}, we assigned a function_id = {function_num}')

        cur.close()
        conn_psy.close()

        return None

    def record_finish_of_function(event_num: int, list_of_changed_ids: list) -> None:
        """Record into PSQL that this function finished working (id = id of the respective pub/sub event)"""

        conn_psy = sql_connect_by_psycopg2()
        cur = conn_psy.cursor()

        json_of_params = json.dumps({'ch_id': list_of_changed_ids})

        sql_text_psy = """
                        UPDATE
                            functions_registry
                        SET
                            time_finish = %s,
                            params = %s
                        WHERE
                            event_id = %s
                        ;
                        /*action='save_finish_of_notif_function' */
                        ;"""

        cur.execute(sql_text_psy, (datetime.datetime.now(), json_of_params, event_num))

        cur.close()
        conn_psy.close()

        return None

    if not context or not event:
        return False

    try:
        event_id = context.event_id
    except Exception as e:  # noqa
        return False

    # if this functions is triggered in the very beginning of the Google Cloud Function execution
    if event == 'start':
        if check_if_other_functions_are_working():
            record_start_of_function(event_id, function_id, triggered_by_func_id)
            return True

        record_start_of_function(event_id, function_id, triggered_by_func_id)
        return False

    # if this functions is triggered in the very end of the Google Cloud Function execution
    elif event == 'finish':
        record_finish_of_function(event_id, changed_ids)
        return False


def finish_time_analytics(notif_times: List, delays: List, parsed_times: List, list_of_change_ids: List):
    """Make final steps for time analytics: inform admin, log, record statistics into PSQL"""

    if not notif_times:
        return None

    # send statistics on number of messages and sending speed

    len_n = len(notif_times)
    average = sum(notif_times) / len_n
    ttl_time = round(sum(notif_times), 1)
    if not delays:
        min_delay, max_delay = None, None
    else:
        min_delay = round(min(delays), 1)
        max_delay = round(max(delays), 1)

    if not parsed_times:
        min_parse_time, max_parse_time = None, None
    else:
        min_parse_time = int(min(parsed_times))
        max_parse_time = int(max(parsed_times))

    message = (
        f'[s1] {len_n} x {round(average, 2)} = {int(ttl_time)} '
        f'| {min_delay}–{max_delay} | {min_parse_time}–{max_parse_time} | {list_of_change_ids}'
    )
    if len_n >= 10:  # FIXME – a temp deactivation to understand the sending speed. # and average > 0.3:
        notify_admin(message)
    logging.info(message)

    # save to psql the analytics on sending speed
    conn_psy = sql_connect_by_psycopg2()
    cur = conn_psy.cursor()

    try:
        sql_text_psy = """
                        INSERT INTO notif_stat_sending_speed
                        (timestamp, num_of_msgs, speed, ttl_time)
                        VALUES
                        (%s, %s, %s, %s);
                        /*action='notif_helper_stat_sending_speed' */
                        ;"""

        cur.execute(sql_text_psy, (datetime.datetime.now(), len_n, average, ttl_time))
    except:  # noqa
        pass

    cur.close()
    conn_psy.close()

    return None


def get_triggering_function(message_from_pubsub: str):
    """get a function_id of the function, which triggered this function (if available)"""

    triggered_by_func_id = None
    try:
        if (
            message_from_pubsub
            and isinstance(message_from_pubsub, dict)
            and 'triggered_by_func_id' in message_from_pubsub.keys()
        ):
            triggered_by_func_id = message_from_pubsub['triggered_by_func_id']

    except Exception as e:
        logging.exception(e)

    if triggered_by_func_id:
        logging.info(f'this function is triggered by func-id {triggered_by_func_id}')
    else:
        logging.info('triggering func_id was not determined')

    return triggered_by_func_id


def main(event, context):
    """Main function that is triggered by pub/sub"""

    global analytics_notif_times
    global analytics_delays
    global analytics_parsed_times

    # timer is needed to finish the script if it's already close to timeout
    script_start_time = datetime.datetime.now()

    function_id = generate_random_function_id()

    message_from_pubsub = process_pubsub_message_v2(event)
    triggered_by_func_id = get_triggering_function(message_from_pubsub)

    there_is_function_working_in_parallel = check_and_save_event_id(
        context, 'start', function_id, None, triggered_by_func_id
    )
    if there_is_function_working_in_parallel:
        logging.info('function execution stopped due to parallel run with another function')
        check_and_save_event_id(context, 'finish', function_id, None, None)
        logging.info('script finished')
        return None

    bot_token = get_app_config().bot_api_token__prod
    admin_id = get_app_config().my_telegram_id

    with requests.Session() as session:
        changed_ids = iterate_over_notifications(bot_token, admin_id, script_start_time, session, function_id)

    finish_time_analytics(analytics_notif_times, analytics_delays, analytics_parsed_times, changed_ids)
    # the below – is needed for high-frequency function execution, otherwise google remembers prev value
    analytics_notif_times = []
    analytics_delays = []
    analytics_parsed_times = []

    check_and_save_event_id(context, 'finish', function_id, changed_ids, None)
    logging.info('script finished')

    return 'ok'
