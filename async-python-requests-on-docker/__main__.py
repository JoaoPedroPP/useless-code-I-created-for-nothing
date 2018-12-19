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
        reti = requests.post("https://openwhisk.ng.bluemix.net/api/v1/namespaces/wcpbr%40br.ibm.com_1542976583157_dev/actions/hecrawl-threat?blocking=true", json=data, auth=HTTPBasicAuth("250a4a31-4aa3-457f-beaf-d742534c8588", "PofhnA5MQ36A7IoYFv3VYoHKUixId9a2wBTvuYweVkzAI4heGJOdlIOGWxx5UoPD"), headers=headers)
        if i == 3:
                time.sleep(5)
        return reti.json()

async def req():
        resps = []
        dado = []
        loop = asyncio.get_event_loop()
        parsed = feedparser.parse('https://threatpost.com/feed/')
        # resps = [loop.create_task(req2({"link": "https://threatpost.com/dell-warns-of-attempted-breach-on-network/139464/","title": "Dell Warns of Attempted Breach on Network","date": "Thu, 29 Nov 2018 00:03:41 +0000"}, 1)) for i in range(1)]
        for i in range(len(parsed['entries'])):
                link = parsed['entries'][i]['link']
                title = parsed['entries'][i]['title']
                date = parsed['entries'][i]['published']
                sys_date = datetime.strptime(date, "%a, %d %b %Y %X %z")
                data = {"link": link, "title": title, "date": date}
                resp = loop.create_task(req2(data,i))
                # resp = req2(data, i)
                # resp_future = loop.run_in_executor(None, req2, data)
                # resp = await resp_future
                resps.append(resp)
        for response in await asyncio.gather(*resps):
                dado.append(response)
                # pass
        # print(resps)
        return dado
def main(dict):
        loop = asyncio.get_event_loop()
        a = loop.run_until_complete(req())
        print(a)
        data = {"data": json.dumps(a)}
        return data
x = main({})
print(x)
# def main(dict):
#         article = []
#         error = []
#         parsed = feedparser.parse('https://threatpost.com/feed/')
#         for i in range(len(parsed['entries'])):
#                 try:
#                         link = parsed['entries'][i]['link']
#                         title = parsed['entries'][i]['title']
#                         date = parsed['entries'][i]['published']
#                         sys_date = datetime.strptime(date, "%a, %d %b %Y %X %z")
#                         data = {"link": link, "title": title, "date": date}
#                         headers = {"Content-Type": "application/json"}
#                         requests.post("https://openwhisk.ng.bluemix.net/api/v1/namespaces/wcpbr%40br.ibm.com_1542976583157_dev/actions/hecrawl-threat?blocking=true", json=data, auth=HTTPBasicAuth("250a4a31-4aa3-457f-beaf-d742534c8588", "PofhnA5MQ36A7IoYFv3VYoHKUixId9a2wBTvuYweVkzAI4heGJOdlIOGWxx5UoPD"), headers=headers)
#                         # asyncio.run(req(data, i))
#                         article.append({"data":data, "index": i})
#                         print("Done")
#                 except:
#                         print("Error")
#                         error.append({"data":data, "index": i})
#         resp = {"done": article, "error":error}
#         print(resp)
#         return resp

# a = main({"link":"link"})
# print(a)