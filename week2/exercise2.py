#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"

import nltk

br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')

WORD, TAG = 0, 1


def main():
    """
    asdadsad
    :return:
    """
    amount_of_words, amount_of_sentences = amount_of_words_and_sentences()
    print("2A. Amount of words and sentences...")
    print("- words: {}".format(amount_of_words))
    print("- sentences: {}".format(amount_of_sentences))
    print()

    print("2B. 50th and 75th words and tags...")
    print(br_tw[49])
    print(br_tw[74])
    print()

    print("2C. Amount of different POS tags...")



def amount_of_words_and_sentences():
    """
    Get the amount of words and amount of sentences.
    :return:
    """
    return len(br_tw), len(br_ts)


if __name__ == '__main__':
    main()
