class Common_Word_Forms_Check:
    def __init__(self, mem_module_fn):
        self.dist = distance.nlevenshtein
        self.csm = self.__contiguous_string_matches__

        # cwf_mem = common word forms memory
        self.cwf_mem_fn = mem_module_fn
        self.cwf_mem = self.__load_object_from_file__(self.cwf_mem_fn)

    def get_base_form_of_word(self, word):
        if word in self.cwf_mem.keys():
            return self.cwf_mem[word]
        else:
            poss_base_words = self.__retrieve_possible_tokens__(word)
            poss_base_words = sorted(set(poss_base_words))

            if poss_base_words:
                self.base_form = min(poss_base_words, key=len)
            else:
                self.base_form = None

            self.cwf_mem[word] = self.base_form
            self.__store_object_to_file__(self.cwf_mem, self.cwf_mem_fn)

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
        # url = f'https://www.dictionary.com/browse/{word}'

        try:
            response = urllib.request.urlopen(url)
        except UnicodeEncodeError:
            poss_tokens = []
            return poss_tokens
        except urllib.error.HTTPError:
            poss_tokens = []
            return poss_tokens
            # print(f'Hit a urllib.error.HTTPError with URL = {url}')

        html = response.read()
        html = html.decode('utf8', 'ignore')
        raw = BeautifulSoup(html, 'html.parser').get_text()
        tokens = nltk.wordpunct_tokenize(raw)

        poss_tokens = sorted(set([
            t.lower() for t in tokens
            if self.dist(t.lower(), word) <= 0.51
            and t.lower() not in STOP_WORDS
            and t.lower() in ENGLISH_WORDS
            and self.csm(word, t.lower())]))

        return poss_tokens

    def __contiguous_string_matches__(self, main_s, s_compare):
        if len(main_s) < len(s_compare):
            main_s, s_compare = s_compare, main_s

        for i in range(len(s_compare)):
            if s_compare[i] != main_s[i]:
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
