import requests
import os
import time
from random import randrange

from barknotify import send_notify

from requests.sessions import session


ACCOUNT = os.environ.get('YOUYUN_ACCOUNT')
PASSWD = os.environ.get('YOUYUN_PASSWD')
SLEEP_TIME_MIN = os.environ.get('YOUYUN_SLEEP_TIME_MIN') or 1
SLEEP_TIME_MAX = os.environ.get('YOUYUN_SLEEP_TIME_MAX') or 6

NOTIFY_GROUP = 'Youyun'

session = requests.Session()


def visitHome():
    url = "https://youyun666.com"

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
        'referer': 'https://youyun666.com',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)


def isSignin():
    return False

def login():
    url = "https://youyun666.com/auth/login"
    payload = "email=%s&passwd=%s&code=" % (ACCOUNT, PASSWD)
    headers = {
    'authority': 'youyun666.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"macOS"',
    'origin': 'https://youyun666.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://youyun666.com/auth/login',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    response = session.request("POST", url, headers=headers, data=payload)
    print(response.text)

def addSignin():
    import requests
    url = "https://youyun666.com/user/checkin"
    payload={}
    headers = {
    'authority': 'youyun666.com',
    'content-length': '0',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'origin': 'https://youyun666.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://youyun666.com/user',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    response = session.request("POST", url, headers=headers, data=payload)
    print(response.text)
    send_notify(NOTIFY_GROUP, response.text)


if ACCOUNT is None:
    print("please set YOUYUN_ACCOUNT")
    send_notify(NOTIFY_GROUP, "please set YOUYUN_ACCOUNT")
    exit(1)
if PASSWD is None:
    print("please set YOUYUN_PASSWD")
    send_notify(NOTIFY_GROUP, "please set YOUYUN_PASSWD")
    exit(1)

sleep_time = randrange(SLEEP_TIME_MIN, SLEEP_TIME_MAX)*10

print("begin to handle youyun task. sleep_time: %ss" % (sleep_time))
send_notify(
    NOTIFY_GROUP, "begin to handle youyun task. sleep_time: %ss" % (sleep_time))
time.sleep(sleep_time)
visitHome()
login()
visitHome()
signin = isSignin()
if(signin):
    print("already signin")
    send_notify(NOTIFY_GROUP, "already signin.")
else:
    time.sleep(randrange(1, SLEEP_TIME_MIN*10))
    addSignin()
    print("finish the youyun task.")
    send_notify(NOTIFY_GROUP, "finish the youyun task.")
