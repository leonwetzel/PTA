#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"

import string
from collections import Counter, OrderedDict
import nltk
from nltk import ngrams

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
    corpus = generate_corpus(data)
    sentences = prepare(corpus)
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

    print("Generating ngrams and removing punctuation...")
    unigrams, bigrams, trigrams  = generate_ngrams(corpus)
    print("Done!", '\n')

    print("Performing 2A: Amount of character types...")
    character_types(unigrams)
    print()

    print("Performing 2B: Amount of word types...")
    word_types(unigrams)
    print()

    print("Performing 2C: Top 20 character-level unigrams, bigrams and trigrams...")
    top_twenty_character_level_unigrams_bigrams_trigrams(unigrams)
    print()

    print("Performing 2D: Top 20 word-level unigrams, bigrams and trigrams...")
    top_twenty_word_level_unigrams_bigrams_trigrams(unigrams)
    print()


def generate_corpus(data):
    """
    Turns the source data into
    :param data:
    :return:
    """
    corpus = [sentence.strip() for sentence in data]
    corpus = list(filter(None, corpus))
    corpus = " ".join(corpus)
    return corpus


def prepare(corpus):
    """
    Restructures the data and generates sentences.
    Sentence tokenization is performed by NLTK's sent_tokenize().
    :param corpus:
    :return: list of sentences and list of ngrams.
    """
    sentences = nltk.sent_tokenize(corpus)
    return sentences


def generate_ngrams(corpus):
    """
    Generates n-grams. Bigrams and trigrams are based on unigrams.
    :param corpus:
    :return:
    """
    unigrams = [
        token.translate(str.maketrans('', '', string.punctuation))
        for token in nltk.word_tokenize(corpus)
    ]
    unigrams = [token for token in unigrams if token]
    bigrams = nltk.bigrams(unigrams)
    trigrams = nltk.trigrams(unigrams)
    return unigrams, bigrams, trigrams


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
    """
    Returns a dictionary containing lengths
    and frequencies of lengths of sentences.
    :param sentences:
    :return:
    """
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


def character_types(unigrams):
    """
    Extracts character types from a given list of unigrams.
    :param unigrams:
    :return:
    """
    types = set(unigrams)
    print("Amount of character types: {}".format(len(types)))
    for character_type in sorted(types):
        print(character_type)


def word_types(unigrams):
    """
    Extracts word types from a given list of unigrams.
    :param unigrams:
    :return:
    """
    types = set([token.lower() for token in unigrams])
    print("Amount of word types: {}".format(len(types)))
    for word_type in sorted(types):
        print(word_type)


def top_twenty_character_level_unigrams_bigrams_trigrams(unigrams):
    print('Generating most frequent character level unigrams...')
    character_level_unigrams = []
    for token in unigrams:
        for letter in token:
            character_level_unigrams.append(letter.lower())
    unigram_dict = Counter(character_level_unigrams)
    for unigram in sorted(unigram_dict, key=unigram_dict.get, reverse = True)[:20]:
        print(unigram)
    print()
    
    print('Generating most frequent character level bigrams...')
    character_level_bigrams = []
    for token in unigrams:
        for letter_index in range(len(token) - 1):
            character_level_bigrams.append(token[letter_index].lower() + token[letter_index + 1].lower())
    bigram_dict = Counter(character_level_bigrams)
    for bigram in sorted(bigram_dict, key=bigram_dict.get, reverse = True)[:20]:
        print(bigram)
    print()
    
    print('Generating most frequent character level trigrams...')
    character_level_trigrams = []
    for token in unigrams:
        for letter_index in range(len(token) - 2):
            character_level_trigrams.append(token[letter_index].lower() + token[letter_index + 1].lower() + token[letter_index + 2])
    trigram_dict = Counter(character_level_trigrams)
    for trigram in sorted(trigram_dict, key=trigram_dict.get, reverse = True)[:20]:
        print(trigram)
    print()
			

			


def top_twenty_word_level_unigrams_bigrams_trigrams(unigrams):
    print('Generating most frequent character level unigrams...')
    unigram_dict = Counter(ngrams(unigrams, 1))
    for unigram in sorted(unigram_dict, key=unigram_dict.get, reverse = True)[:20]:
        print(*unigram)
    print()
    
    print('Generating most frequent character level bigrams...')
    bigram_dict = Counter(ngrams(unigrams, 2))
    for bigram in sorted(bigram_dict, key=bigram_dict.get, reverse = True)[:20]:
        print(*bigram)
    print()
    
    print('Generating most frequent character level trigrams...')
    trigram_dict = Counter(ngrams(unigrams, 3))
    for trigram in sorted(trigram_dict, key=trigram_dict.get, reverse = True)[:20]:
        print(*trigram)
    print()


if __name__ == '__main__':
    main()
