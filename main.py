import os
import json
from contextlib import redirect_stdout

import requests as rq
from bs4 import BeautifulSoup as bs
import re
from dataclasses import dataclass
@dataclass
class Video:
    id : int
    title : str
    author : str
    description : str

def write_json(table,outputname):
    with open(outputname,'w') as ou:
        json.dump(table,ou)
def read_json(filename):
    with open(filename,'r') as input:
        return 1

def parse_vide(video_id):
    url = "https://www.youtube.com/watch?v="+video_id
    soup = bs(rq.get(url).text,"html.parser")


url = "https://www.youtube.com/watch?v=JwSCjUaa3DU"
source = requests.get(url).text
soup = bs(source, 'html.parser')
div_s = soup.findAll('div')
span_s = soup.findAll('span')
Title = div_s[0].find("meta",{"itemprop":"name"}).get("content")
Author = div_s[0].find("link",{"itemprop":"name"}).get("content")
description = re.compile('(?<=shortDescription":").*(?=","isCrawlable)').findall(str(soup))[0].replace('\\n','\n')
#likes = soup.find("div", class_="cbox yt-spec-button-shape-next--button-text-content").span.button.text
likes = source[:source.find(' aime"')]
var = likes[likes.rfind('"') + 1:]
print(var)

#print(likes)
#print(description)
print(Title)
print(Author)
with open('out.txt', 'w') as f:
    with redirect_stdout(f):
        print(soup)