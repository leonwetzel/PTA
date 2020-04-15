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

    sentences = prepare(data)
    lengths = {sentence: len(sentence) for sentence in sentences}

    print("Performing 1A: Longest sentence...")
    print(longest_sentence(lengths))

    print("Performing 1B: Shortest sentence...")
    print(shortest_sentence(lengths))


def prepare(data):
    """
    Restructures the data and generates sentences.
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
    :param sentences:
    :return:
    """
    return sorted(lengths, key=lengths.get, reverse=True)[0]


def shortest_sentence(lengths):
    """
    Returns the shortest sentence in the corpus.
    :param sentences:
    :return:
    """
    return sorted(lengths, key=lengths.get, reverse=True)[-1]


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
