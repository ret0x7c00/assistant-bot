#!/usr/bin/python3

import requests
import time
from random import randrange
import json
import os

# auth token
AUTH_TOKEN = os.environ.get('DUOLINGO_AUTH_TOKEN')
TOTAL_CNT_MIN = os.environ.get('DUOLINGO_TOTAL_CNT_MIN') or 3
TOTAL_CNT_MAX = os.environ.get('DUOLINGO_TOTAL_CNT_MAX') or 15
SLEEP_TIME_MIN = os.environ.get('DUOLINGO_SLEEP_TIME_MIN') or 1
SLEEP_TIME_MAX = os.environ.get('DUOLINGO_SLEEP_TIME_MAX') or 6


def get_question():
    # 获取题目
    url = "https://www.duolingo.cn/2017-06-30/sessions"

    payload = "{\n    \"fromLanguage\": \"zh\",\n    \"learningLanguage\": \"en\",\n    \"challengeTypes\": [\n        \"characterIntro\",\n        \"characterMatch\",\n        \"characterSelect\",\n        \"completeReverseTranslation\",\n        \"definition\",\n        \"dialogue\",\n        \"form\",\n        \"freeResponse\",\n        \"gapFill\",\n        \"judge\",\n        \"listen\",\n        \"name\",\n        \"listenComprehension\",\n        \"listenTap\",\n        \"readComprehension\",\n        \"select\",\n        \"selectPronunciation\",\n        \"selectTranscription\",\n        \"tapCloze\",\n        \"tapComplete\",\n        \"tapDescribe\",\n        \"translate\"\n    ],\n    \"type\": \"GLOBAL_PRACTICE\",\n    \"juicy\": false\n}"
    headers = {
        'Authorization': AUTH_TOKEN,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json',
        'Referer': 'http://www.duolingo.cn/practice',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3572.0 Safari/537.36',
        'Connection': 'keep-alive'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    respJson = response.json()
    return respJson


def put_answer(respJson):
    # 提交答案
    url2 = "https://www.duolingo.cn/2017-06-30/sessions/"+respJson["id"]

    now = int(time.time())

    respJson["startTime"] = now-900
    respJson["endTime"] = now
    respJson["failed"] = False
    respJson["max_in_lesson_streak"] = randrange(13, 20)
    respJson["heartsLeft"] = 0

    payload2 = json.dumps(respJson, separators=(
        ',', ':'), ensure_ascii=False).encode('utf8')
    headers = {
        'Authorization': AUTH_TOKEN,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json',
        'Referer': 'http://www.duolingo.cn/practice',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3572.0 Safari/537.36',
        'Connection': 'keep-alive'
    }

    response2 = requests.request("PUT", url2, headers=headers, data=payload2)
    print(response2)


total_cnt = randrange(TOTAL_CNT_MIN, TOTAL_CNT_MAX)
print("total count: %s" % (total_cnt))

for cnt in range(1, total_cnt):
    sleep_time = randrange(SLEEP_TIME_MIN, SLEEP_TIME_MAX)*60

    if AUTH_TOKEN is None:
        print("please set DUOLINGO_AUTH_TOKEN")
        break
    print("the %s times is waiting for %ss" % (cnt, sleep_time))
    respJson = get_question()
    # print(respJson)
    # 延迟1~5分钟
    time.sleep(sleep_time)
    put_answer(respJson)
    time.sleep(randrange(10, 60))
