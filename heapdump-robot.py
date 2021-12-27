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


def visitHome():
    url = "https://www.heapdump.cn/"

    payload = {}
    headers = {
        'authority': 'www.heapdump.cn',
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
        'referer': 'https://www.heapdump.cn/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)


def isSignin():
    url = "https://www.heapdump.cn/api/community/signin/isSignin"

    payload = {}
    headers = {
        'authority': 'www.heapdump.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': 'application/json, text/plain, */*',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.heapdump.cn/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'UM_distinctid=17af291f8c49ad-098284a7075cca-35637203-13c680-17af291f8c5b77; _ga=GA1.2.1179930627.1635835930; Hm_lvt_3408298b960e49eb328fcacc70d124c5=1638237736,1639967025,1640093361,1640223854; CNZZDATA1278052687=740206226-1627565290-https%253A%252F%252Fheapdump.cn%252F%7C1640569458; _gid=GA1.2.344283848.1640569459; serviceTicket=760214901c414424b6e97df00d1f393e; JSESSIONID=4C7C163F68D083FEFC3485BC53E208A6; Hm_lpvt_3408298b960e49eb328fcacc70d124c5=1640575072'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response.json().get('data')

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
visitHome()
login()
visitHome()
signin = isSignin()
if(signin):
    print("already signin")
    send_notify("Heapdump", "already signin.")
else:
    time.sleep(randrange(1, SLEEP_TIME_MIN*10))
    addSignin()
    print("finish the heapdump task.")
    send_notify("Heapdump", "finish the heapdump task.")
