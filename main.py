import os
import json
import requests
from bs4 import BeautifulSoup
import re
url = "https://www.youtube.com/watch?v=JwSCjUaa3DU"
Vid = {}
Link = url
source= requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
div_s = soup.findAll('div')
Title = div_s[0].find("meta",{"itemprop":"name"}).get("content")
Author = div_s[0].find("link",{"itemprop":"name"}).get("content")
pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
description = pattern.findall(str(soup))[0].replace('\\n','\n')
print(description)
print(Title)
print(Author)