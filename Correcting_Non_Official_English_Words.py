from bs4 import BeautifulSoup
import urllib
import nltk
import pprint
import requests

pp = pprint.PrettyPrinter(indent=2)


def __get_correct_english_word__(word):
    url = f'https://www.merriam-webster.com/dictionary/{word}'

    html = urllib.request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')

    the_word = soup.find_all('h1', class_="hword")[0].get_text()
    print(the_word)
    # print(word, len(big_list), big_list)
    # for an_item in big_list:
    #     print('\t', an_item.get_text())

    # return html
    # return page.content
    # print(soup.prettify())
    # return soup


word_list = [
    'processability', 'resistant', 'processing', 'resistance',
    'resistivity', 'thermally', 'thermodynamics', 'thermodynamic',
    'flammability']

for word in word_list:
    __get_correct_english_word__(word)
