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
from nltk import wordpunct_tokenize
from nltk.collocations import BigramCollocationFinder


def main():
    with open('holmes.txt') as file:
        text = file.read()

    tokens = wordpunct_tokenize(text)
    print(tokens)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    scored = finder.score_ngrams(bigram_measures.raw_freq())

    sorted_values = sorted([bigram for bigram, score in scored])

    print(sorted_values)


def most_likely_20_collocations_by_pmi(collocations):
    pass


def most_likely_20_collocations_by_chi_square(collocations):
    pass


def compare_top_20_bigrams():
    pass


def calculate_spearman_coefficient():
    pass


if __name__ == '__main__':
    main()
