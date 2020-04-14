#!/usr/bin/python3
import nltk


def main():
    """
    Script for assignment 1 of week 1 for the course Project Text Analysis.
    This script processes holmes.txt and retrieves information such as

    :return:
    """
    with open("holmes.txt", "rt") as file:
        data = file.readlines()

    sentences, ngrams = prepare(data)


def prepare(data):
    """
    Cleans the data and generates sentences and n-grams.
    :param data:
    :return: list of sentences and list of ngrams.
    """
    sentences, ngrams = [], []

    sentences = [sentence.strip() for sentence in data]
    sentences = list(filter(None, sentences))
    sentences = " ".join(sentences)

    print(sentences)

    return sentences, ngrams


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
