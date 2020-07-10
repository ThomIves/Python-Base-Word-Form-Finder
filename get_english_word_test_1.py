from bs4 import BeautifulSoup
# import urllib
# import nltk
# import distance
# import os
# import json
# import sys
# import pprint

import requests


word = 'electricals'
url = f'https://www.merriam-webster.com/dictionary/{word}'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.get_text())


# class Muscle_Get_URL:
#     def __init__(self):
#         user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#         user_agent_string += 'AppleWebKit/537.36 (KHTML, like Gecko) '
#         user_agent_string += 'Chrome/80.0.3987.163 '
#         user_agent_string += 'Safari/537.36'
#
#         acc_str = "text/html, application/xhtml+xml,"
#         acc_str += "application/xml;q=0.9,*/*;q=0.8"
#
#         self.hdrs = {'User-Agent': user_agent_string,
#                      'Accept-Language': 'en-US,en;q=0.9',
#                      "Upgrade-Insecure-Requests": "1",
#                      "DNT": "1",
#                      "Accept": acc_str,
#                      "Accept-Encoding": "gzip, deflate"}
#
#     def get_url_status(self, url):
#         url_dict = self.__get_url_dict__(url)
#
#         for key in ('orig', 'base', 'com_base', 'surl'):
#             curr_url = url_dict.get(key)
#             if curr_url:
#                 the_code, the_content = \
#                     self.__get_reqs_url_status__(key, curr_url)
#             if key == 'orig':
#                 orig_code = the_code
#                 orig_content = the_content
#             if the_code == 200:
#                 return url, the_code, the_content
#
#         return url, orig_code, orig_content
#
#     def __get_url_dict__(self, url):
#         url_dict = {'orig': url}
#         url_clean = url.rstrip('/')
#         shortest = url_clean
#         url_list = url_clean.split('/')
#         url_length = len(url_list)
#         if url_length > 3:
#             url_dict['base'] = '/'.join(url_list[:3])
#             shortest = url_dict['base']
#         if 'com' in shortest:
#             com_base_url_list = shortest.split('.')
#             try:
#                 com_index = com_base_url_list.index('com')
#                 crap_after_com = com_index + 1 < len(com_base_url_list)
#                 if crap_after_com:
#                     com_base_url = '.'.join(com_base_url_list[:com_index+1])
#                     url_dict['com_base'] = com_base_url
#                     shortest = url_dict['com_base']
#             except ValueError:
#                 pass
#         url_dict['surl'] = shortest.replace('http:', 'https:')
#
#         return url_dict
#
#     def __get_reqs_url_status__(self, key, url):
#         try:
#             jar = requests.cookies.RequestsCookieJar()
#             jar.set('cookie_one', 'one', domain=url, path='/cookies')
#             page = requests.get(
#                 url, cookies=jar, timeout=10.0, headers=self.hdrs,
#                 verify=pem_path)
#             the_code = page.status_code
#             if page.text:
#                 the_content = (key, url)
#
#             if page.history:  # and the_code != 200:
#                 url = page.url
#                 page = requests.get(
#                     url, cookies=jar, timeout=10.0, headers=self.hdrs,
#                     verify=pem_path)
#                 the_code = page.status_code
#                 the_content = (f'Redirect from {key}', url)
#         except Exception:
#             the_code, the_content = 'NONE', ('NONE', 'NONE')
#
#         return the_code, the_content
#
#     def __get_async_url_status__(self, key, url):
#         loop = asyncio.get_event_loop()
#         task = loop.create_task(
#             self.__do_async_ops__(key, url))
#         loop.run_until_complete(task)
#         the_code, the_content = task.result()
#
#         return the_code, the_content
#
#     async def __do_async_ops__(self, key, url):
#         timeout = aiohttp.ClientTimeout(total=60)
#         async with aiohttp.ClientSession(timeout=timeout) as client:
#             try:
#                 async with client.get(url) as response:
#                     the_code = response.status
#                     page_text = await response.text()
#                     if page_text:
#                         the_content = (f'Asyncio on {key}', url)
#             except Exception:
#                 the_code, the_content = 'NONE', ('NONE', 'NONE')
#
#             return the_code, the_content
#
#
# STOP_WORDS = nltk.corpus.stopwords.words('english')
# ENGLISH_WORDS = nltk.corpus.words.words()
# pp = pprint.PrettyPrinter(indent=2)
# mgurl = Muscle_Get_URL()

# try:
#     html = urllib.request.urlopen(url).read().decode('utf8')
#     soup = BeautifulSoup(html, 'html.parser')
#     the_word = soup.find_all('h1', class_="hword")[0].get_text()
# except urllib.error.HTTPError:
#     url, the_code, the_content = mgurl.get_url_status(url)
#     print(url)
#     print(the_code)
#     print()
#     print(the_content)
#
# print(the_word)
