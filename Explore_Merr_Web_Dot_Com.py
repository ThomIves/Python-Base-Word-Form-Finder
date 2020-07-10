from bs4 import BeautifulSoup
import urllib
import requests
import nltk
import string
import distance
import os
import json
import sys
import time
import pprint

pp = pprint.PrettyPrinter(indent=2)

spr_hdr = {}
spr_hdr['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
spr_hdr['User-Agent'] += 'AppleWebKit/537.36 (KHTML, like Gecko) '
spr_hdr['User-Agent'] += 'Chrome/56.0.2924.76 Safari/537.36'
spr_hdr['Upgrade-Insecure-Requests'] = '1'
spr_hdr["DNT"] = "1"
spr_hdr["Accept"] = "text/html,application/xhtml+xml,application/xml;"
spr_hdr["Accept"] += "q=0.9,*/*;q=0.8"
spr_hdr["Accept-Language"] = "en-US,en;q=0.5"
spr_hdr["Accept-Encoding"] = "gzip, deflate"
super_headers = spr_hdr

word = 'flammable'
url = f'https://www.merriam-webster.com/dictionary/{word}'

# response = requests.get(url)
page = requests.get(url, headers=super_headers)
if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    # with open('thermodynamics.merrweb.com.txt', 'w', encoding="utf-8") as f:
    # f.write(response.text)
    # f.write(soup.prettify())
    s0 = soup.find('p', class_="et")
    pp.pprint(s0.get_text())
