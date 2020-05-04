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
    """
    Prepares the txt file and turns it into tokens.
    """
    with open('holmes.txt') as file:
        text = file.read()
    tokens = wordpunct_tokenize(text)
    most_likely_20_collocations_by_pmi(tokens)
    most_likely_20_collocations_by_chi_sq(tokens)


def most_likely_20_collocations_by_pmi(tokens):
    """
    Generates the 20 most likely collocations.
    """
    print('Generating 20 most likely collocations using PMI...')
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    scored_pmi = finder.score_ngrams(bigram_measures.pmi)
    for i in scored_pmi[:20]:
        print(*i)
    print()


def most_likely_20_collocations_by_chi_sq(tokens):
    """
    Generates the 20 most likely collocations.
    """
    print('Generating 20 most likely collocations using chi squared...')
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    scored_chi_sq = finder.score_ngrams(bigram_measures.chi_sq)
    for i in scored_chi_sq[:20]:
        print(*i)
    print()


if __name__ == '__main__':
    main()
