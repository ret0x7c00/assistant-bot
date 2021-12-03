import requests
import os
import time
from random import randrange

from barknotify import send_notify

from requests.sessions import session


ACCOUNT = os.environ.get('HEAPDUMP_ACCOUNT')
PASSWD = os.environ.get('HEAPDUMP_PASSWD')
SLEEP_TIME_MIN = os.environ.get('HEAPDUMP_SLEEP_TIME_MIN') or 1
SLEEP_TIME_MAX = os.environ.get('HEAPDUMP_SLEEP_TIME_MAX') or 6

session = requests.Session()


def login():
    login_url = "https://www.heapdump.cn/api/login/authentication/v1/login"
    payload = "{\"account\":\"%s\",\"passwd\":\"%s\"}" % (ACCOUNT, PASSWD)
    headers = {
        'authority': 'www.heapdump.cn',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4741.0 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://www.heapdump.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.heapdump.cn/',
        'accept-language': 'en-US,en;q=0.9',
    }
    response = session.request(
        "POST", login_url, headers=headers, data=payload)
    print(response.text)


def addSignin():
    signin_url = "https://www.heapdump.cn/api/community/signin/addSignin"
    payload = {}
    headers = {
        'authority': 'www.heapdump.cn',
        'content-length': '0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4741.0 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://www.heapdump.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.heapdump.cn/',
        'accept-language': 'en-US,en;q=0.9',
    }
    response = session.request(
        "POST", signin_url, headers=headers, data=payload)
    print(response.text)
    send_notify("Heapdump", response.text)


if ACCOUNT is None:
    print("please set HEAPDUMP_ACCOUNT")
    send_notify("Heapdump", "please set HEAPDUMP_ACCOUNT")
    exit(1)
if PASSWD is None:
    print("please set HEAPDUMP_PASSWD")
    send_notify("Heapdump", "please set HEAPDUMP_PASSWD")
    exit(1)

sleep_time = randrange(SLEEP_TIME_MIN, SLEEP_TIME_MAX)*10

print("begin to handle heapdump task. sleep_time: %ss" % (sleep_time))
send_notify(
    "Heapdump", "begin to handle heapdump task. sleep_time: %ss" % (sleep_time))
time.sleep(sleep_time)
login()
time.sleep(randrange(1, SLEEP_TIME_MIN*10))
addSignin()
print("finish the heapdump task.")
send_notify("Heapdump", "finish the heapdump task.")
