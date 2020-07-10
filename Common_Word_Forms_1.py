from urllib import request
from bs4 import BeautifulSoup
import nltk
import distance
import pprint

pp = pprint.PrettyPrinter(indent=2)


def contiguous_string_matches(main_s, s_compare):
    if len(main_s) < len(s_compare):
        main_s, s_compare = s_compare, main_s

    for i in range(len(s_compare)):
        if s_compare[i] != main_s[i]:
            return False

    return True


csm = contiguous_string_matches

word = 'processability'
word = 'resistant'
url = f'https://www.merriam-webster.com/dictionary/{word}'

dist = distance.nlevenshtein

html = request.urlopen(url).read().decode('utf8')
raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = nltk.wordpunct_tokenize(raw)  # nltk.word_tokenize

poss_tokens = [t.lower() for t in tokens
               if dist(t.lower(), word) <= 0.51
               and csm(word, t.lower())]
poss_tokens = sorted(set(poss_tokens))

pp.pprint(poss_tokens)


###############################################################################
# url = "http://www.gutenberg.org/files/2554/2554-0.txt"
# response = request.urlopen(url)
# raw = response.read().decode('utf8')
# print(type(raw))
# print(len(raw))
# print(raw[:75])
