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
    urls: str
    timestamps: str


def write_json(table, output_name):
    with open(output_name, 'w') as ou:
        for i in table:
            json.dump(i.__dict__, ou)


def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)["video_id"]


def extract_urls(string):
    urls = re.findall('(?P<url>https?://[^\s]+)', string)
    return (urls)


def extract_timestamps(string):
    timestamps = re.findall(r'(.*\d{2}:\d{2}?.*)', string)
    return timestamps


def parse_video(video_id):
    video_url = "https://www.youtube.com/watch?v=" + video_id
    soup = bs(rq.get(video_url).text, "html.parser")
    div_s = soup.findAll('div')
    video_title = div_s[0].find("meta", {"itemprop": "name"}).get("content")
    video_author = div_s[0].find("link", {"itemprop": "name"}).get("content")
    video_description = re.compile('(?<=shortDescription":").*(?=","isCrawlable)').findall(str(soup))[0].replace('\\n',
                                                                                                                 '\n')
    urls = extract_urls(video_description)
    timestamps = extract_timestamps(video_description)
    return Video(id=video_id, title=video_title, author=video_author, description=video_description, urls=urls,
                 timestamps=timestamps)
    write_json()


l = []
videos = read_json("input.json")
for i in videos:
    l.append(parse_video(i))
print(l[0].id)
write_json(l, "out.json")
