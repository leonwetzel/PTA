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

    score_similarity()

    amount_of_nouns_referring_to_relative()
    amount_of_nouns_referring_to_illness()
    amount_of_nouns_referring_to_science()


def amount_of_nouns_referring_to_relative():
    relative_lemma = lemmatizer.lemmatize('relative')
    synsets = wordnet.synsets(relative_lemma)
    print('The amount of nouns referring to the word relative is: {}'.format(len(synsets)))
    print()


def amount_of_nouns_referring_to_illness():
    illness_lemma = lemmatizer.lemmatize('illness')
    synsets = wordnet.synsets(illness_lemma)
    print('The amount of nouns referring to the word illness is: {}'.format(len(synsets)))
    print()


def amount_of_nouns_referring_to_science():
    science_lemma = lemmatizer.lemmatize('science')
    synsets = wordnet.synsets(science_lemma)
    print('The amount of nouns referring to the word science is: {}'.format(len(synsets)))
    print()


def amount_of_hypernyms_per_noun(noun_lemmas):
    """
    1. In how many cases was there only one hypernym per noun? Give a couple of
    examples, indicating the noun and its hypernym.
    2. In how many cases did your system had to choose among more than one
    possi-ble hypernyms?  Give a couple of examples, and specify which
    hypernyms wereavailable.
    3. What is the average number of hypernyms per noun in the whole text?
    :return:
    """
    one_hypernym_list = []
    more_hypernyms_list = []
    for noun in noun_lemmas[:-1]:
        synsets = wordnet.synsets(noun, pos='n')
        hypernym_list = []
        for synset in synsets:
            hypernym = synset.hypernyms()
            if hypernym and hypernym not in hypernym_list:
                hypernym_list.append(hypernym)
        if len(hypernym_list) == 1:
            one_hypernym_list.append([noun, hypernym_list])
        if len(hypernym_list) > 1:
            more_hypernyms_list.append([noun, hypernym_list])
    print('Printing nouns with one hypernym and corresponing hypernym')
    print(one_hypernym_list)
    print()
    print('Printing nouns with more than one hypernyms and corresponing hypernyms')
    print(more_hypernyms_list)
    print()
    hypernyms = len(one_hypernym_list)
    for more_hypernym_noun in more_hypernyms_list:
        hypernyms += len(more_hypernym_noun[1])
    average_hypernyms = hypernyms / len(noun_lemmas)
    print('The average hypernyms per word in the text is:')
    print(average_hypernyms)
    print()


def score_similarity():
    """
    Use one or more of the predefined similarity measures in the NLTK corpus reader for
    WordNet to score the similarity of each of these word pairs. Rank the pairs in order
    of decreasing similarity and discuss how close your ranking is to the one obtained
    experimentally by Miller and Charles.

    Note that what matters is the ranking, not the actual scores.

    :return:
    """
    car = wordnet.synset('car.n.01')
    automobile = wordnet.synset('automobile.n.01')
    coast = wordnet.synset('coast.n.01')
    shore = wordnet.synset('shore.n.01')
    food = wordnet.synset('food.n.01')
    fruit = wordnet.synset('fruit.n.01')
    journey = wordnet.synset('journey.n.01')
    monk = wordnet.synset('monk.n.01')
    slave = wordnet.synset('slave.n.01')
    moon = wordnet.synset('moon.n.01')
    string = wordnet.synset('string.n.01')

    synset_list_path = [('car-automobile', car.path_similarity(automobile)), ('coast-shore', coast.path_similarity(shore)),
                        ('food-fruit', food.path_similarity(fruit)), ('journey-car', journey.path_similarity(car)),
                        ('monk-slave', monk.path_similarity(slave)), ('moon-string', moon.path_similarity(string))]

    synset_list_lch = [('car-automobile', car.lch_similarity(automobile)), ('coast-shore', coast.lch_similarity(shore)),
                       ('food-fruit', food.lch_similarity(fruit)), ('journey-car', journey.lch_similarity(car)),
                       ('monk-slave', monk.lch_similarity(slave)), ('moon-string', moon.lch_similarity(string))]

    print('Path Similarity\n')
    for item in sorted(synset_list_path, key=lambda x: x[1], reverse=True):
        print(item)

    print('\nLeacock-Chodorow Similarity\n')
    for item in sorted(synset_list_lch, key=lambda x: x[1], reverse=True):
        print(item)


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
