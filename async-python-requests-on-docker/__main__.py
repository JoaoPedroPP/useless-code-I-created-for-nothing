import sys
from datetime import datetime
import requests
import feedparser
import asyncio
import json
import time

from requests.auth import HTTPBasicAuth

async def req2(data, i):
        headers = {"Content-Type": "application/json"}
        reti = requests.post("https://", json=data, auth=HTTPBasicAuth("user", "password"), headers=headers)
        if i == 3:
                time.sleep(5)
        return reti.json()

async def req():
        resps = []
        dado = []
        loop = asyncio.get_event_loop()
        parsed = feedparser.parse('https://threatpost.com/feed/')
        for i in range(len(parsed['entries'])):
                link = parsed['entries'][i]['link']
                title = parsed['entries'][i]['title']
                date = parsed['entries'][i]['published']
                sys_date = datetime.strptime(date, "%a, %d %b %Y %X %z")
                data = {"link": link, "title": title, "date": date}
                resp = loop.create_task(req2(data,i))
                resps.append(resp)
        for response in await asyncio.gather(*resps):
                dado.append(response)
                pass
        return dado
def main(dict):
        loop = asyncio.get_event_loop()
        a = loop.run_until_complete(req())
        print(a)
        data = {"data": json.dumps(a)}
        return data

x = main({})
print(x)