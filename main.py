# Downloader for ubicast media servers

import os
import sys
import re
import requests
import json

# input your api key which you can find following this guide https://ubicast.tv/static/mediaserver/docs/api/index.html#authentication
api_key = "pUMbY-n4erd-j4sT7-AqQY4-cpYEN"
ubicast_server = "https://medias.unamur.be/"
try:
    url = sys.argv[1]
except IndexError:
    print(f"Usage:\
        {sys.argv[0]} <permalink>")
    exit()

oid = re.sub('.*permalink',"", url).strip("/")
params = {
    "api_key": api_key,
    "oid": oid,
    "html5": "mp4_mp3_m3u8"
}

res = requests.get(f"{ubicast_server}/api/v2/medias/modes/", params=params, verify=False)
dict_vid = json.loads(res.content)
url_vid = dict_vid["720p"]["resource"]["url"]
url_audio = dict_vid["audio"]["tracks"][0]["url"]

params.pop("html5")
res = requests.get(f"{ubicast_server}/api/v2/medias/get/", params=params, verify=False)
info_vid = json.loads(res.content)
title = info_vid["info"]["title"]

os.system(f"ffmpeg -i '{url_vid}' -i '{url_audio}' -bsf:a aac_adtstoasc -c:v copy -c:a copy {title}.mkv")
