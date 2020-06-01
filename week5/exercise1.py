#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"

from collections import Counter

import wikipedia
import os

from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag, sent_tokenize
from nltk.wsd import lesk


def main():
    page_id_list = []
    for subdir, dirs, files in os.walk('gold standard'):
        for file in files:
            extension = os.path.splitext(file)[-1].lower()
            if '.ent' in extension:
                # deduct file name and instantiate variables
                offsets_start, offsets_end = [], []
                ids, tokens = [], []
                input_file_name = os.path.join(subdir, file)
                with open(input_file_name, 'r') as F:
                    token_rows = F.readlines()
               
                for i in token_rows:
                    if len(i.split()) == 7:
                        if i.split()[6].split('/')[-1] not in page_id_list:
                            page_id_list.append(i.split()[6].split('/')[-1])

    for page_id in page_id_list:
        print(f"Page {page_id}")
        try:
            page = wikipedia.page(page_id)
        except wikipedia.exceptions.DisambiguationError:
            pass
        except wikipedia.exceptions.PageError:
            pass
        sentences = sent_tokenize(page.content)
        for sentence in sentences:
            tokens = word_tokenize(sentence)
            pos_tags = pos_tag(tokens)
            for item in pos_tags:
                if item[1][0] == 'N':
                    token = item[0]
                    if len(wordnet.synsets(token, 'n')) > 1:
                        print(token, lesk(sentence, token, 'n'), len(wordnet.synsets(token, 'n')))

    print(f"{len(page_id_list)} pages have been used.")


if __name__ == '__main__':
    main()
