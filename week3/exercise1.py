#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"


from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def main():
    """
    Performs assignment 1.
    """
    print("ASSIGNMENT 3 - PART 1")
    print("==============================================\n")

    with open("ada_lovelace.txt", 'r') as file:
        corpus = file.read()

    tokens = word_tokenize(corpus)
    pos_tags = pos_tag(tokens)

    noun_lemmas = []
    for item in pos_tags:
        if item[1][0] == 'N':
            lemma = lemmatizer.lemmatize(item[0], wordnet.NOUN)
            noun_lemmas.append(lemma)


def amount_of_nouns_referring_to_relative():
    pass


def amount_of_nouns_referring_to_illness():
    pass


def amount_of_nouns_referring_to_science():
    pass


def amount_of_hypernyms_per_noun():
    """
    In how many cases was there only one hypernym per noun? Give a couple of
    examples, indicating the noun and its hypernym
    :return:
    """
    pass


def amount_of_chosen_possible_hypernyms():
    """
    In how many cases did your system had to choose among more than one possible
    hypernyms? Give a couple of examples, and specify which hypernyms were
    available
    :return:
    """
    pass


def average_number_of_hypernyms_per_noun():
    """
    What is the average number of hypernyms per noun in the whole text?
    :return:
    """
    pass


def score_similarity():
    """
    Use one or more of the predefined similarity measures in the NLTK corpus reader for
    WordNet to score the similarity of each of these word pairs. Rank the pairs in order
    of decreasing similarity and discuss how close your ranking is to the one obtained
    experimentally by Miller and Charles.

    Note that what matters is the ranking, not the actual scores.

    :return:
    """
    pass


def is_hypernym_of(synset1, synset2):
    """
    Returns True if synset2 is a hypernym of
    synset1, or if they are the same synset.

    :return: False otherwise.
    """
    if synset1 == synset2:
        return True
    for hypernym in synset1.hypernyms():
        if synset2 == hypernym:
            return True
        if is_hypernym_of(hypernym, synset2):
            return True
        return False


if __name__ == '__main__':
    main()
