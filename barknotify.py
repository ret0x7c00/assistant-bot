#!/usr/bin/python3

import requests
import os

AUTH_TOKEN = os.environ.get('BARK_AUTH_TOKEN')


def send_notify(msg):
    if AUTH_TOKEN is None:
        print('Bark auth token not found.')
        return
    url = "https://api.day.app/"+AUTH_TOKEN+"/Duolinguo/"+msg+"?group=Duolinguo"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# send_notify("hello")
