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


def __contiguous_string_matches__(main_s, s_compare):
    if len(main_s) < len(s_compare):
        main_s, s_compare = s_compare, main_s

    total = 0
    for i in range(len(s_compare)):
        if s_compare[i] == main_s[i]:
            total += 1
        else:
            break  # To ensure only contiguous matches are counted

    if total / len(s_compare) < 0.8:
        return False

    return total


STOP_WORDS = nltk.corpus.stopwords.words('english')
ENGLISH_WORDS = nltk.corpus.words.words()
PUNCS = string.punctuation
pp = pprint.PrettyPrinter(indent=2)
csm = __contiguous_string_matches__

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

word = 'thermodynamics'
url = f'https://en.wikipedia.org/wiki/{word}'

t0 = time.time()
response = requests.get(url, headers=super_headers)
t1 = time.time()
print(f'{t1-t0} seconds to get response.')
soup = BeautifulSoup(response.text, 'html.parser')
t2 = time.time()
print(f'{t2-t1} seconds to soupify response.')

s0 = soup.get_text()
t3 = time.time()
print(f'{t3-t2} seconds to get text from soup')

for punc in PUNCS:
    s0 = s0.replace(punc, ' ')
t4 = time.time()
print(f'{t4-t3} to spacify puncs')

s0 = s0.split()
t5 = time.time()
print(f'{t5-t4} seconds listify')

s0 = [t.lower() for t in s0]
t6 = time.time()
print(f'{t6-t5} to lower case')

s0 = [t for t in s0 if t not in STOP_WORDS]
t7 = time.time()
print(f'{t7-t6} seconds to remove stop words')

s0 = s0
t8 = time.time()
print(f'{t8-t7} seconds to NOT reduce to english - english source')

s0 = [t for t in s0 if csm(word, t)]
t9 = time.time()
print(f'{t9-t8} seconds to ensure contiguous matches')

s0 = [t for t in s0 if len(t) <= len(word)]
t10 = time.time()
print(f'{t10-t9} to check lengths')

s0 = sorted(set(s0))
t11 = time.time()
print(f'{t11-t10} to reduce and sort those items.')
print(f'{t11-t0} for the complete process.')

pp.pprint(s0)

min_length = len(min(s0, key=len))
best_words = [w for w in s0 if len(w) == min_length]
best_scores = [csm(w, word) for w in best_words]

print(best_words)
print(best_scores)
best_words_D = dict(zip(best_scores, best_words))
best_word = best_words_D[max(best_words_D.keys())]
print(best_word)

# Results
# 0.29001522064208984 seconds to get response.
# 0.1460094451904297 seconds to soupify response.
# 0.0030002593994140625 seconds to get text from soup
# 0.0 to spacify puncs
# 0.0009996891021728516 seconds listify
# 0.001001119613647461 to lower case
# 0.013999700546264648 seconds to remove stop words
# 0.0 seconds to NOT reduce to english - english source
# 0.005000114440917969 seconds to ensure contiguous matches
# 0.0 to check lengths
# 0.0 to reduce and sort those items.
# 0.4600255489349365 for the complete process.
# ['therme', 'thermo', 'thermodynamic', 'thermodynamics']
# ['therme', 'thermo']
# [5, 6]
# thermo
