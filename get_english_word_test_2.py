from bs4 import BeautifulSoup
import requests
import nltk
import distance
import sys
import pprint

STOP_WORDS = nltk.corpus.stopwords.words('english')
ENGLISH_WORDS = nltk.corpus.words.words()
pp = pprint.PrettyPrinter(indent=2)


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

    return True


csm = __contiguous_string_matches__
word = 'electricals'
url = f'https://www.merriam-webster.com/dictionary/{word}'

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

response = requests.get(url, headers=spr_hdr)
soup = BeautifulSoup(response.text, 'html.parser')

stuff = soup.find('div', id="near-entries-anchor")
if not stuff:
    other_stuff = soup.find('p', class_="spelling-suggestions")
    new_stuff = other_stuff.get_text().split()
    print(new_stuff)
    # print(f'Should use {the_word} instead')
    sys.exit()
text = stuff.get_text()
text = text.replace('Dictionary Entries near ', '')
text = text.replace(' See More Nearby Entries', '')
poss_base_words = text.split()

poss_base_words = [t.lower() for t in poss_base_words]
print(poss_base_words)
print()

poss_base_words = sorted(set([
    t for t in poss_base_words
    if t not in STOP_WORDS
    and t in ENGLISH_WORDS
    and csm(word, t)
    and len(t) <= len(word)]))

print(poss_base_words)
