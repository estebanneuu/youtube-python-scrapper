import os
import json
from contextlib import redirect_stdout

import requests as rq
from bs4 import BeautifulSoup as bs
import re
from dataclasses import dataclass
import pandas as pd


@dataclass
class Video:
    id: int
    title: str
    author: str
    description: str


def write_json(table, outputname):
    with open(outputname, 'w') as ou:
        for i in table:
            json.dump(i.__dict__, ou)


def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)["video_id"]



def parse_video(video_id):
    video_url = "https://www.youtube.com/watch?v=" + video_id
    soup = bs(rq.get(video_url).text, "html.parser")
    div_s = soup.findAll('div')
    video_title = div_s[0].find("meta", {"itemprop": "name"}).get("content")
    video_author = div_s[0].find("link", {"itemprop": "name"}).get("content")
    video_description = re.compile('(?<=shortDescription":").*(?=","isCrawlable)').findall(str(soup))[0].replace('\\n',
                                                                                                                 '\n')
    return Video(id=video_id, title=video_title, author=video_author, description=video_description)
    write_json()

l = []
videos = read_json("input.json")
for i in videos:
    l.append(parse_video(i))
print(l[0].id)
write_json(l,"out.json")
