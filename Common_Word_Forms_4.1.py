from bs4 import BeautifulSoup
from word_forms.word_forms import get_word_forms
import urllib
import requests
import nltk
import string
import distance
import os
import json
import sys
import pprint

STOP_WORDS = nltk.corpus.stopwords.words('english')
ENGLISH_WORDS = nltk.corpus.words.words()
PUNCS = string.punctuation
pp = pprint.PrettyPrinter(indent=2)

# <section class="css-pnw38j e1hk9ate0">


class Common_Word_Forms_Check:
    def __init__(self, mem_module_fn):
        self.dist = distance.nlevenshtein
        self.csm = self.__contiguous_string_matches__

        # cwf_mem = common word forms memory
        self.cwf_mem_fn = mem_module_fn
        # self.cwf_mem = self.__load_object_from_file__(self.cwf_mem_fn)
        self.cwf_mem = {}

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
        self.super_headers = spr_hdr

    def get_base_form_of_word(self, word):
        if word in self.cwf_mem.keys():
            return self.cwf_mem[word]

        poss_base_words = self.__retrieve_possible_merr_web_tokens__(word)
        # poss_base_words += self.__retrieve_possible_wiki_tokens__(word)

        if poss_base_words:
            self.base_form = self.__closest_poss_base_word__(
                word, poss_base_words)
        else:
            self.base_form = None

        self.cwf_mem[word] = self.base_form
        self.__store_object_to_file__(self.cwf_mem, self.cwf_mem_fn)

        return self.base_form

    def __purge_poss_base_words__(self, word, poss_base_words):
        poss_base_words = sorted(set([
            t for t in poss_base_words
            if t not in STOP_WORDS and self.csm(word, t)
            and len(t) <= len(word) and len(t) > 1]))

        return poss_base_words

    def __closest_poss_base_word__(self, word, poss_base_words, metric=''):
        min_metric = 100000.0

        if not poss_base_words:
            return None
        elif len(poss_base_words) == 1:
            return poss_base_words[0]

        min_length = len(min(poss_base_words, key=len))
        best_words = [w for w in poss_base_words if len(w) == min_length]
        best_scores = [self.csm(w, word) for w in best_words]

        best_words_D = dict(zip(best_scores, best_words))
        best_word = best_words_D[max(best_words_D.keys())]

        return best_word

    def __retrieve_possible_merr_web_tokens__(self, word):
        url = f'https://www.merriam-webster.com/dictionary/{word}'

        response = requests.get(url, headers=self.super_headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        s0 = soup.find('h1', class_="hword")  # s0 = soup_0, etc.
        s1 = soup.find('div', id="near-entries-anchor")
        s2 = soup.find('p', class_="spelling-suggestions")

        poss_base_words = []

        if s1:
            s1 = s1.get_text()
            s1 = s1.replace('Dictionary Entries near ', '')
            s1 = s1.replace(' See More Nearby Entries', '')
            # Remove PUNCS between words
            for punc in PUNCS:
                s1 = s1.replace(punc, ' ')
            s1 = s1.split()
            if s0 and s0 not in s1:
                # print(s0)
                s1.append(s0.get_text())
                # print('\t', s1)
            poss_base_words += [t.lower() for t in s1]

        if s2:
            s2 = s2.get_text().split()
            if s0 and s0 not in s2:
                s2.append(s0.get_text())
            poss_base_words += [t.lower() for t in s2]

        poss_base_words = self.__purge_poss_base_words__(word, poss_base_words)
        poss_base_words = [w for w in poss_base_words if w in ENGLISH_WORDS]

        return poss_base_words

    def __retrieve_possible_wiki_tokens__(self, word):
        # nxns - not exact name string
        nxns = 'Wikipedia does not have an article with this exact name'
        url = f'https://en.wikipedia.org/wiki/{word}'

        response = requests.get(url, headers=self.super_headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        s0 = soup.get_text()  # s0 = soup 0

        if nxns in s0:  # No wiki page or wiki redirect for this word
            return []

        for punc in PUNCS:
            s0 = s0.replace(punc, ' ')

        poss_base_words = s0.split()
        poss_base_words = [t.lower() for t in poss_base_words]
        poss_base_words = self.__purge_poss_base_words__(word, poss_base_words)

        return poss_base_words

    def __contiguous_string_matches__(self, main_s, s_compare):
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

    def __load_object_from_file__(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding="utf-8") as f:
                object = json.load(f)
        else:
            object = {}

        return object

    def __store_object_to_file__(self, object, file_name):
        with open(file_name, 'w', encoding="utf-8") as f:
            json.dump(object, f, ensure_ascii=False, indent=4)


w_list = [
    'chemical', 'chemically', 'electricals', 'electrical', 'fda', 'ul',
    'processability', 'resistant', 'processing', 'resistance',
    'resistivity', 'thermally', 'thermodynamics', 'thermodynamic',
    'flammability', 'gubber', 'recyclable', 'compostable',
    "softening", "processed", "divided", "light", "park", "contained",
    "reduce", "human", "entrust", "personnel", 'entrustable', 'reduceable',
    'thermodynamically']

# w_list = ["softening"]

cwfc = Common_Word_Forms_Check('cwf_mem.cwf')

for w1 in w_list:
    print(f'The base form of "{w1}" is "{cwfc.get_base_form_of_word(w1)}".')
