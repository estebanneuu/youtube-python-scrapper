import asyncio
import json
import time
from unittest import result

from bs4 import BeautifulSoup as bs
from dataclasses import dataclass
import re
from requests_html import AsyncHTMLSession, HTML


@dataclass
class Video:
    id: str
    title: str
    author: str
    likes: str
    description: str
    urls: list
    timestamps: list


def write_json(table, output_name):
    with open(output_name, 'w', encoding='utf8') as ou:
        for video in table:
            json.dump(video.__dict__, ou, ensure_ascii=False)


async def read_file():
    filename = "output.json"
    with open(filename, "r") as file:
        return json.load(file)


async def extract_timestamps(string):
    timestamps = re.findall(r'(.*\d{2}:\d{2}?.*)', string)
    return timestamps


async def extract_urls(string):
    urls = re.findall('(?P<url>https?://[^\s]+)', string)
    return urls


async def extract_args():
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


async def scrape(url: str, id: str):
    asession = AsyncHTMLSession()
    r = await asession.get(url)

    await r.html.arender(sleep=3)
    soup = bs(r.html.html, "html.parser")
    div_s = soup.findAll('div')
    video_title = div_s[0].find("meta", {"itemprop": "name"}).get("content")
    video_author = div_s[0].find("link", {"itemprop": "name"}).get("content")
    video_description = re.compile('(?<=shortDescription":").*(?=","isCrawlable)').findall(str(soup))[
        0].replace('\\n',
                   '\n')
    likes = soup.select_one('button.yt-spec-button-shape-next--icon-leading > '
                            '.yt-spec-button-shape-next--button-text-content > span.yt-core-attributed-string').contents
    likes = likes[0].replace("&nbsp", "")
    urls = await extract_urls(video_description)
    timestamps = await extract_timestamps(video_description)
    await asyncio.sleep(1)
    await asession.close()
    return Video(id=id, title=video_title, author=video_author, description=video_description, urls=urls,
                 timestamps=timestamps, likes=likes)



async def main():
    start_time = time.time()
    tasks = []
    with open("input.json", 'r') as f:
        for i in json.load(f)["video_id"]:
            task = asyncio.create_task(scrape("https://www.youtube.com/watch?v=" + i, i))
            tasks.append(task)

    print('Saving the output of extracted information')
    write_json(await asyncio.gather(10, *tasks), "output.json")
    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f seconds.' % time_difference)
    # print(await asyncio.gather(*tasks))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
