import requests
import os
import time
from random import randrange

from barknotify import send_notify

from requests.sessions import session


ACCOUNT = os.environ.get('HEAPDUMP_ACCOUNT')
PASSWD = os.environ.get('HEAPDUMP_PASSWD')
SLEEP_TIME_MIN = os.environ.get('HEAPDUMP_SLEEP_TIME_MIN') or 1
SLEEP_TIME_MAX = os.environ.get('HEAPDUMP_SLEEP_TIME_MAX') or 60

NOTIFY_GROUP = 'Heapdump2'

session = requests.Session()


def visitHome():
    url = "https://heapdump.cn/"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }
    response = session.request("GET", url, headers=headers, data=payload)
    print(response.status_code)


def isSignin():
    url = "https://heapdump.cn/api/community/signin/isSignin"

    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://heapdump.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }

    response = session.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response.json().get('data')


def login():
    login_url = "https://heapdump.cn/api/login/authentication/v1/login"
    payload = "{\"account\":\"%s\",\"passwd\":\"%s\"}" % (ACCOUNT, PASSWD)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://heapdump.cn',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://heapdump.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers'
    }
    response = session.request(
        "POST", login_url, headers=headers, data=payload)
    print(response.text)


def addSignin():
    signin_url = "https://heapdump.cn/api/community/signin/addSignin"
    payload = {}
    headers = {
        'authority': 'heapdump.cn',
        'content-length': '0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://heapdump.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://heapdump.cn/',
        'accept-language': 'en-US,en;q=0.9',
    }
    response = session.request(
        "POST", signin_url, headers=headers, data=payload)
    print(response.text)
    send_notify(NOTIFY_GROUP, response.text)


if ACCOUNT is None:
    print("please set HEAPDUMP_ACCOUNT")
    send_notify(NOTIFY_GROUP, "please set HEAPDUMP_ACCOUNT")
    exit(1)
if PASSWD is None:
    print("please set HEAPDUMP_PASSWD")
    send_notify(NOTIFY_GROUP, "please set HEAPDUMP_PASSWD")
    exit(1)

sleep_time = randrange(SLEEP_TIME_MIN, SLEEP_TIME_MAX)*10

print("begin to handle heapdump task. sleep_time: %ss" % (sleep_time))
send_notify(
    NOTIFY_GROUP, "begin to handle heapdump task. sleep_time: %ss" % (sleep_time))
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
    print("finish the heapdump task.")
    send_notify(NOTIFY_GROUP, "finish the heapdump task.")
