import os
import base64
from google.cloud import secretmanager
import requests
import re
import urllib.parse
from time import sleep
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup, Bot
import psycopg2
import datetime
import logging

project_id = os.environ["GCP_PROJECT"]
client = secretmanager.SecretManagerServiceClient()
session = requests.Session()
cur = None
conn_psy = None


class ForumUser:
    def __init__(self,
                 user_id=None,
                 username=None,
                 callsign=None,
                 region=None,
                 phone=None,
                 auto_num=None,
                 age=None,
                 sex=None,
                 reg_date=None,
                 firstname=None,
                 lastname=None
                 ):
        self.user_id = user_id
        self.username = username
        self.callsign = callsign
        self.region = region
        self.phone = phone
        self.auto_num = auto_num
        self.age = age
        self.sex = sex
        self.reg_date = reg_date
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return str([self.user_id, self.username, self.firstname, self.lastname, self.callsign, self.region, self.phone,
                    self.auto_num, self.age,
                    self.sex, self.reg_date])


def get_secrets(secret_request):
    name = f"projects/{project_id}/secrets/{secret_request}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")


def sql_connect_by_psycopg2():
    global cur
    global conn_psy

    db_user = get_secrets("cloud-postgres-username")
    db_pass = get_secrets("cloud-postgres-password")
    db_name = get_secrets("cloud-postgres-db-name")
    db_conn = get_secrets("cloud-postgres-connection-name")
    db_host = '/cloudsql/' + db_conn

    conn_psy = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_pass)
    cur = conn_psy.cursor()


def login_into_forum(forum_bot_password):
    """login in into the forum"""

    global session

    login_page = "https://lizaalert.org/forum/ucp.php?mode=login"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': 'telegram_bot',
        'password': forum_bot_password,
        'login': 'Вход'
    }

    response = session.get(login_page)

    content = response.content.decode("utf-8")

    creation_time_match = re.compile(r'<input.*?name="creation_time".*?value="([^"]*)".*?/>').search(content)
    if creation_time_match:
        data.update({'creation_time': creation_time_match.group(1)})

    redirect_match = re.compile(r'<input.*?name="redirect".*?value="([^"]*)".*?/>').search(content)
    if redirect_match:
        data.update({'redirect': redirect_match.group(1)})

    sid_match = re.compile(r'<input.*?name="sid".*?value="([^"]*)".*?/>').search(content)
    if sid_match:
        data.update({'sid': sid_match.group(1)})

    form_token_match = re.compile(r'<input.*?name="form_token".*?value="([^"]*)".*?/>').search(content)
    if form_token_match:
        data.update({'form_token': form_token_match.group(1)})

    form_data = urllib.parse.urlencode(data)

    sleep(1)  # без этого не сработает %)
    r = session.post(login_page, headers=headers, data=form_data)

    if "Личные сообщения" in r.text:
        print("Logged in successfully")
    # elif "Ошибка отправки формы" in r.text:
    #    print("Form submit error")
    else:
        print('Login Failed')

    return None


def get_user_id(u_name):
    """get user_id from forum"""

    user_id = 0
    forum_prefix = 'https://lizaalert.org/forum/memberlist.php?username='
    user_search_page = forum_prefix + u_name

    r2 = session.get(user_search_page)
    soup = BeautifulSoup(r2.content, features="html.parser")

    try:
        block_with_username = soup.find('a', {'class': 'username'})
        if block_with_username is None:
            block_with_username = soup.find('a', {'class': 'username-coloured'})

        if block_with_username is not None:
            u_string = str(block_with_username)
            user_id = u_string[u_string.find(';u=') + 3:u_string.find('">')]
            if user_id.find('style="color:') != -1:
                user_id = user_id[:(user_id.find('style="color:') - 2)]
            print('User found, user_id=', user_id)
        else:
            user_id = 0
            print('User not found')

    except Exception as e:
        print('User not found, exception:', repr(e))
        user_id = 0

    return user_id


def get_user_attributes(user_id):
    """get user data from forum"""

    url_prefix = 'https://lizaalert.org/forum/memberlist.php?mode=viewprofile&u='
    r3 = session.get(url_prefix + user_id)
    soup = BeautifulSoup(r3.content, features="html.parser")
    block_with_user_attr = soup.find('div', {'class': 'page-body'})

    return block_with_user_attr


def get_user_data(data):
    """aggregates User Profile from forums' data"""

    global user

    dict = {'age': 'Возраст:',
            'sex': 'Пол:',
            'region': 'Регион:',
            'phone': 'Мобильный телефон:',
            'reg_date': 'Зарегистрирован:',
            'callsign': 'Позывной:'
            }

    for attr in dict:
        try:
            value = data.find('dt', text=dict[attr]).findNext('dd').text
            setattr(user, attr, value)
        except Exception as e1:
            print(attr, 'is not defined')
            logging.info(e1)

    return None


def main(event, context):
    """main function triggered from communicate script via pyb/sub"""

    global user
    global cur
    global conn_psy

    user = ForumUser()

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    encoded_to_ascii = eval(pubsub_message)
    data_in_ascii = encoded_to_ascii['data']
    message_in_ascii = data_in_ascii['message']
    tg_user_id, f_username = list(message_in_ascii)

    # initiate Prod Bot
    bot_token = get_secrets("bot_api_token__prod")
    bot = Bot(token=bot_token)

    # log in to forum
    bot_forum_pass = get_secrets('forum_bot_password')
    login_into_forum(bot_forum_pass)

    user_found = False

    if message_in_ascii:
        f_usr_id = get_user_id(f_username)

        if f_usr_id != 0:
            block_of_user_data = get_user_attributes(f_usr_id)
            user_found = True

            if block_of_user_data:
                get_user_data(block_of_user_data)

    if user_found:
        bot_message = 'Посмотрите, Бот нашел следующий аккаунт на форуме, это Вы?\n'
        bot_message += 'username: ' + f_username + ', '
        if user.callsign:
            bot_message += 'позывной: ' + user.callsign + ', '
        if user.region:
            bot_message += 'регион: ' + user.region + ', '
        if user.phone:
            bot_message += 'телефон оканчивается на ' + str(user.phone)[-5:] + ', '
        if user.age:
            bot_message += 'возраст: ' + str(user.age) + ', '
        if user.reg_date:
            bot_message += 'дата регистрации: ' + str(user.reg_date)[:-7] + ', '
        bot_message = bot_message[:-2]

        keyboard = [['да, это я'], ['нет, это не я'], ['в начало']]

        sql_connect_by_psycopg2()

        # Delete previous records for this user
        cur.execute("""DELETE FROM user_forum_attributes WHERE user_id=%s;""", (tg_user_id,))
        conn_psy.commit()

        # Add new record for this user
        cur.execute("""INSERT INTO user_forum_attributes 
        (user_id, forum_user_id, status, timestamp, forum_username, forum_age, forum_sex, forum_region, 
        forum_auto_num, forum_callsign, forum_phone, forum_reg_date) 
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                    (tg_user_id, f_usr_id, 'non-varified', datetime.datetime.now(), f_username, user.age, user.sex,
                     user.region, user.auto_num, user.callsign, user.phone, user.reg_date))
        conn_psy.commit()

    else:
        bot_message = 'Бот не смог найти такого пользователя на форуме. ' \
                      'Пожалуйста, проверьте правильность написания имени пользвателя (логина). ' \
                      'Важно, чтобы каждый знак в точности соответсовал тому, что указано в вашем профиле на форуме'
        keyboard = [['в начало']]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.sendMessage(chat_id=tg_user_id, text=bot_message, reply_markup=reply_markup, parse_mode='HTML')

    # save bot's reply to incoming request
    if bot_message:
        cur.execute("""INSERT INTO dialogs (user_id, author, timestamp, message_text) values (%s, %s, %s, %s);""",
                    (tg_user_id, 'bot', datetime.datetime.now(), bot_message))
        conn_psy.commit()

    cur.close()
    conn_psy.close()

    return None
