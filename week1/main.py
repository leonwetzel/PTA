#!/usr/bin/python3
import nltk


def main():
    """
    Script for assignment 1 of week 1 for the course Project Text Analysis.
    This script processes holmes.txt and retrieves information such as

    :return:
    """
    with open("holmes.txt") as file:
        data = file.read()

    print(data)


def prepare(data):
    pass


def longest_sentence(sentences):
    pass


def shortest_sentence(sentences):
    pass


def sentence_length_distribution(sentences):
    pass


def average_sentence_length(sentences):
    pass


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
