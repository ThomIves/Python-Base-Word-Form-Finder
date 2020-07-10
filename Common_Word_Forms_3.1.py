from bs4 import BeautifulSoup
import urllib
import requests
import nltk
import distance
import os
import json
import sys
import pprint

STOP_WORDS = nltk.corpus.stopwords.words('english')
ENGLISH_WORDS = nltk.corpus.words.words()
pp = pprint.PrettyPrinter(indent=2)


class Common_Word_Forms_Check:
    def __init__(self, mem_module_fn):
        self.dist = distance.nlevenshtein
        self.csm = self.__contiguous_string_matches__

        # cwf_mem = common word forms memory
        self.cwf_mem_fn = mem_module_fn
        self.cwf_mem = self.__load_object_from_file__(self.cwf_mem_fn)

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
        # elif word not in ENGLISH_WORDS:
        #     eng_word = self.__get_correct_english_word__(word)
        #     if not eng_word:
        #         return None
            # print(f'\tUsing "{eng_word}" in place of "{word}"')
        # else:
        #     eng_word = word

        poss_base_words = self.__retrieve_possible_tokens__(word)
        poss_base_words = sorted(set(poss_base_words))
        # pp.pprint(poss_base_words)

        if poss_base_words:
            if word in poss_base_words and len(poss_base_words) > 1:
                poss_base_words.remove(word)
            # self.base_form = min(poss_base_words, key=len)
            self.base_form = self.__closest_poss_base_word__(
                word, poss_base_words)
        else:
            self.base_form = None

        self.cwf_mem[word] = self.base_form
        self.__store_object_to_file__(self.cwf_mem, self.cwf_mem_fn)

        # print(self.base_form)
        # sys.exit()
        return self.base_form

    def words_have_common_base_form(self, word_1, word_2):
        poss_tokens_1 = self.__retrieve_possible_tokens__(word_1)
        poss_tokens_2 = self.__retrieve_possible_tokens__(word_2)

        poss_tokens = list(set(poss_tokens_1) & set(poss_tokens_2))

        if poss_tokens:
            self.base_form = min(poss_tokens, key=len)
            return True
        else:
            self.base_form = None
            return False

    def __get_poss_tokens__(self, word, text):
        poss_tokens = nltk.wordpunct_tokenize(text)

        poss_tokens = [t.lower() for t in poss_tokens]
        poss_tokens = sorted(set([
            t for t in poss_tokens
            if self.dist(t, word) <= 0.73
            and t not in STOP_WORDS
            and t in ENGLISH_WORDS
            and self.csm(word, t)
            and len(t) <= len(word)
            and len(t) > 1]))

        return poss_tokens

    def __closest_poss_base_word__(self, word, poss_base_words, metric=''):
        min_metric = 100000.0
        for w in poss_base_words:
            if not metric:
                the_metric = len(w)
            elif metric == 'min_dist':
                the_metric = abs(len(w) - len(word))

            if the_metric < min_metric:
                min_metric = the_metric
                best_word = w
                # print('\t', word, the_metric, best_word)

        try:
            return best_word
        except UnboundLocalError:
            # print('HIT UnboundLocalError while trying to return best word.')
            # print(f'Best word not set for {word}.')
            # print(f'Possible best words passed in were: {poss_base_words}')
            # sys.exit()
            return None

    def __ultra_stupid_word_correction__(self, url):
        response = requests.get(url, headers=self.super_headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        return text

    def __get_correct_english_word__(self, word):
        url = f'https://www.merriam-webster.com/dictionary/{word}'

        try:
            html = urllib.request.urlopen(url).read().decode('utf8')
            soup = BeautifulSoup(html, 'html.parser')
            the_word = soup.find_all('h1', class_="hword")[0].get_text()
            return the_word
        except urllib.error.HTTPError:
            html = self.__ultra_stupid_word_correction__(url)
            poss_base_words = self.__get_poss_tokens__(word, html)
            the_word = self.__closest_poss_base_word__(
                word, poss_base_words, metric='min_dist')
            return the_word
            # print(f'Performed ultra stupid search for {word}.')

    def __retrieve_possible_tokens__(self, word):
        urls = [
            f'https://en.wikipedia.org/wiki/{word}',
            f'https://www.merriam-webster.com/dictionary/{word}',
            f'https://www.dictionary.com/browse/{word}']

        poss_tokens = []
        for url in urls:
            # print('\t', url)
            try:
                html = urllib.request.urlopen(url).read().decode('utf8')
            except UnicodeEncodeError:
                poss_tokens = []
                return poss_tokens
            except urllib.error.HTTPError:
                try:
                    eng_word = self.__get_correct_english_word__(word)
                    if not eng_word:
                        continue
                    url = url.replace(word, eng_word)
                    html = urllib.request.urlopen(url).read().decode('utf8')
                except urllib.error.HTTPError:
                    # print('HIT urllib.error.HTTPError:')
                    # print(f'Replaced {word} with {eng_word}', )
                    # print('and still could not find it.')
                    # print(f'I last looked at {url}')
                    # sys.exit()
                    continue

            raw = BeautifulSoup(html, 'html.parser').get_text()
            poss_tokens = self.__get_poss_tokens__(word, raw)

            if not poss_tokens:
                continue
            break

        return poss_tokens

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

        return True

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
    'chemical', 'electricals', 'electrical', 'fda', 'ul',
    'processability', 'resistant', 'processing', 'resistance',
    'resistivity', 'thermally', 'thermodynamics', 'thermodynamic',
    'flammability', 'gubber', 'recyclable', 'compostable']

cwfc = Common_Word_Forms_Check('cwf_mem.cwf')

for w1 in w_list:
    print(f'The base form of "{w1}" is "{cwfc.get_base_form_of_word(w1)}".')
