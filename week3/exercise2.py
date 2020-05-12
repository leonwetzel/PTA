#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"


import requests

from nltk import word_tokenize, pos_tag, wordnet
from nltk.parse import CoreNLPParser
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.corpus import wordnet as wn

lemmatizer = WordNetLemmatizer()


def main():
    """
    This script performs part 3 of exercise 2.

    Pick the model you prefer, and using both the NER tagger and WordNet information,
    classify all nouns or NP chunks in the text using the classes expressed by your classifier
    (for example, picking the classifier from the box above, this would mean classifying all
    nouns or NP chunks into one of Person, Organization, Location.)

    :return:
    """
    ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')

    with open("ada_lovelace.txt", 'r') as file:
        corpus = file.read()

    tokens = word_tokenize(corpus)
    pos_tags = pos_tag(tokens)
    synsets, named_entities = {}, []

    noun_lemmas = []
    for item in pos_tags:
        if item[1][0] == 'N':
            lemma = lemmatizer.lemmatize(item[0], wordnet.NOUN)
            noun_lemmas.append(lemma)
            synsets[lemma] = wn.synsets(lemma, pos="n")

    named_entities = ner_tagger.tag(noun_lemmas)

    for key, value in synsets.items():
        words = {synset.name().split('.')[0] for synset in value}

        if words:
            named_entities.extend(ner_tagger.tag(words))

    for word, named_entity in set(named_entities):
        print(word, named_entity)


if __name__ == '__main__':
    main()
