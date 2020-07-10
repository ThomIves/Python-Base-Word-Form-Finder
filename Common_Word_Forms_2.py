from urllib import request
from bs4 import BeautifulSoup
import nltk
import distance


class Common_Word_Forms_Check:
    def __init__(self):
        self.dist = distance.nlevenshtein
        self.csm = self.__contiguous_string_matches__

    def get_base_form_of_word(self, word):
        poss_base_words = self.__retrieve_possible_tokens__(word)
        poss_base_words = sorted(set(poss_base_words))

        if poss_base_words:
            self.base_form = min(poss_base_words, key=len)
        else:
            self.base_form = None

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

    def __retrieve_possible_tokens__(self, word):
        url = f'https://www.merriam-webster.com/dictionary/{word}'
        html = request.urlopen(url).read().decode('utf8')
        raw = BeautifulSoup(html, 'html.parser').get_text()
        tokens = nltk.wordpunct_tokenize(raw)

        poss_tokens = sorted(set([
            t.lower() for t in tokens
            if self.dist(t.lower(), word) <= 0.51
            and self.csm(word, t.lower())]))

        return poss_tokens

    def __contiguous_string_matches__(self, main_s, s_compare):
        if len(main_s) < len(s_compare):
            main_s, s_compare = s_compare, main_s

        for i in range(len(s_compare)):
            if s_compare[i] != main_s[i]:
                return False

        return True


w1 = 'chemically'  # 'resistant'  # 'processing'
w2 = 'chemicals'  # 'resistance'  # 'processability'

cwfc = Common_Word_Forms_Check()

print(f'The base form of {w1} is {cwfc.get_base_form_of_word(w1)}.')
print(f'The base form of {w2} is {cwfc.get_base_form_of_word(w2)}.')
print()

c_base = cwfc.words_have_common_base_form(w1, w2)
if c_base:
    print(f'The common base form of "{w1}" and "{w2}" is "{cwfc.base_form}".')
else:
    print(f'The words "{w1}" and "{w2}" have do NOT have a common base form.')
