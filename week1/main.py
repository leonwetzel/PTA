#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buisje@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"

from collections import Counter, OrderedDict
import nltk

LENGTH, SENTENCE = 0, 1
counter = Counter()


def main():
    """
    Script for assignment 1 of week 1 for the course Project Text Analysis.
    This script processes holmes.txt and retrieves information such as
    amount of sentences, length of sentences and n-grams.
    :return:
    """
    print("Reading file...")
    with open("holmes.txt", "rt") as file:
        data = file.readlines()
    print("Done!", '\n')

    print("Preparing data...")
    sentences = prepare(data)
    sorted_lengths = sorted([(len(sentence), sentence) for sentence in sentences])
    print("Done!", '\n')

    print("Performing 1A: Longest sentence, semi-based on alphabetical order...")
    print(longest_sentence(sorted_lengths), '\n')

    print("Performing 1B: Shortest sentence, semi-based on alphabetical order...")
    print(shortest_sentence(sorted_lengths), '\n')

    print("Performing 1C: Distribution of sentence lengths...")
    distribution = sentence_length_distribution(sorted_lengths)
    for length, frequency in distribution.items():
        print("Length = {}, count = {}".format(length, frequency))
    print()

    print("Performing 1D: Average sentence length in amount of characters...")
    print(average_sentence_length(sorted_lengths), '\n')

    print("Performing 2A: Amount of character types...")
    print()

    print("Performing 2B: Amount of word types...")
    print()

    print("Performing 2C: Top 20 character-level unigrams, bigrams and trigrams...")
    print()

    print("Performing 2D: Top 20 word-level unigrams, bigrams and trigrams...")
    print()


def prepare(data):
    """
    Restructures the data and generates sentences.
    Sentence tokenization is performed by NLTK's sent_tokenize().
    :param data:
    :return: list of sentences and list of ngrams.
    """
    sentences = [sentence.strip() for sentence in data]
    sentences = list(filter(None, sentences))
    sentences = " ".join(sentences)
    sentences = nltk.sent_tokenize(sentences)
    return sentences


def longest_sentence(lengths):
    """
    Returns the longest sentence in the corpus.
    Length is based on the amount of characters
    in a sentence.
    :param lengths:
    :return:
    """
    return lengths[-1][SENTENCE]


def shortest_sentence(lengths):
    """
    Returns the shortest sentence in the corpus.
    Length is based on the amount of characters
    in a sentence.
    :param lengths:
    :return:
    """
    return lengths[0][SENTENCE]


def sentence_length_distribution(sentences):
    for sentence in sentences:
        counter[sentence[LENGTH]] += 1
    return OrderedDict(counter)


def average_sentence_length(sentences):
    """
    Returns the average sentence length,
    based on the amount of characters in sentences.
    :param sentences:
    :return:
    """
    lengths = [sentence[LENGTH] for sentence in sentences]
    return sum(lengths) / len(lengths)


def character_types(ngrams):
    pass


def word_types(ngrams):
    pass


def top_twenty_character_level_unigrams_bigrams_trigrams(ngrams):
    pass


def top_twenty_word_level_unigrams_bigrams_trigrams(ngrams):
    pass


if __name__ == '__main__':
    main()
