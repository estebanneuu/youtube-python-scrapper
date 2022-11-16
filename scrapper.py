import argparse
import json
from typing import List
from bs4 import BeautifulSoup as bs
import re
from dataclasses import dataclass
from requests_html import HTMLSession

import aiohttp

HEADERS = {'User-Agent': 'Mozilla/5.0'}

@dataclass
class Video:
    id: int
    title: str
    author: str
    likes: str
    description: str
    urls: list
    timestamps: list


def write_json(table, output_name):
    with open(output_name, 'w') as ou:
        for video in table:
            json.dump(video.__dict__, ou)


def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)["video_id"]


def extract_urls(string):
    urls = re.findall('(?P<url>https?://[^\s]+)', string)
    return (urls)


def extract_timestamps(string):
    timestamps = re.findall(r'(.*\d{2}:\d{2}?.*)', string)
    return timestamps


def extract_args():
    parser = argparse.ArgumentParser()  # on crée un objet parser
    parser.add_argument('--input', help='Input JSON file with video IDs',
                        required=True)
    parser.add_argument('--output', help='Output JSON file with parsed datas',
                        required=True)
    args = parser.parse_args()
    argdict = vars(args)
    input_parameter = argdict['input']
    output_parameter = argdict['output']
    return input_parameter, output_parameter


async def get_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            return await resp.text()


def parse_video(video_id):
    video_url = "https://www.youtube.com/watch?v=" + video_id
    session = HTMLSession()
    response = session.get(video_url)
    response.html.render(sleep=2)

    soup = bs(response.html.html, "lxml")
    div_s = soup.findAll('div')

    video_title = div_s[0].find("meta", {"itemprop": "name"}).get("content")
    video_author = div_s[0].find("link", {"itemprop": "name"}).get("content")
    video_description = re.compile('(?<=shortDescription":").*(?=","isCrawlable)').findall(str(soup))[0].replace('\\n',
                                                                                                                 '\n')
    urls = extract_urls(video_description)
    timestamps = extract_timestamps(video_description)
    likes = soup.select_one('button.yt-spec-button-shape-next--icon-leading > '
                            '.yt-spec-button-shape-next--button-text-content > span.yt-core-attributed-string')
    if likes == "None":
        likes = 0
    else: likes = likes.content
    return Video(id=video_id, title=video_title, author=video_author, description=video_description, urls=urls,
                 timestamps=timestamps, likes=likes)


extract_args()
l: List[Video] = []
videos = read_json("input.json")
for i in videos:
    l.append(parse_video(i))
write_json(l, "output.json")
