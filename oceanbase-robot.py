import requests
import os
import time
from random import randrange

from barknotify import send_notify

from requests.sessions import session


COOKIE = os.environ.get('OCEANBASE_COOKIE')
SLEEP_TIME_MIN = os.environ.get('OCEANBASE_SLEEP_TIME_MIN') or 1
SLEEP_TIME_MAX = os.environ.get('OCEANBASE_SLEEP_TIME_MAX') or 6

NOTIFY_GROUP = 'OCEANBASE'

session = requests.Session()


def visitHome():
    url = "https://www.oceanbase.com"

    payload = {}
    headers = {
        'authority': 'www.youyun.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.oceanbase.com',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)


def isSignin():
    return False

def addSignin():
    url = "https://www.oceanbase.com/api/insert/user/signUp"
    payload = "{}"
    headers = {
    'authority': 'www.oceanbase.com',
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'content-type': 'application/json; charset=utf-8',
    'sec-gpc': '1',
    'origin': 'https://open.oceanbase.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://open.oceanbase.com/',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': "%s" % COOKIE
    }
    response = session.request("POST", url, headers=headers, data=payload)
    print(response.text)
    send_notify(NOTIFY_GROUP, response.text)


if COOKIE is None:
    print("please set OCEANBASE_COOKIE")
    send_notify(NOTIFY_GROUP, "please set OCEANBASE_COOKIE")
    exit(1)

sleep_time = randrange(SLEEP_TIME_MIN, SLEEP_TIME_MAX)*10

print("begin to handle oceanbase task. sleep_time: %ss" % (sleep_time))
send_notify(
    NOTIFY_GROUP, "begin to handle oceanbase task. sleep_time: %ss" % (sleep_time))
time.sleep(sleep_time)
visitHome()
signin = isSignin()
if(signin):
    print("already signin")
    send_notify(NOTIFY_GROUP, "already signin.")
else:
    time.sleep(randrange(1, SLEEP_TIME_MIN*10))
    addSignin()
    print("finish the oceanbase task.")
    send_notify(NOTIFY_GROUP, "finish the oceanbase task.")
visitHome()
