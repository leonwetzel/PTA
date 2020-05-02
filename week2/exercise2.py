#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"

from collections import Counter

import nltk

br_tw = nltk.corpus.brown.tagged_words(categories='mystery')
br_ts = nltk.corpus.brown.tagged_sents(categories='mystery')

WORD, TAG = 0, 1


def main():
    """
    asdadsad
    :return:
    """
    amount_of_words, amount_of_sentences = amount_of_words_and_sentences()
    print("2A. Amount of words and sentences...")
    print("- words: {}".format(amount_of_words))
    print("- sentences: {}".format(amount_of_sentences))
    print()

    print("2B. 50th and 75th words and tags...")
    print(br_tw[49])
    print(br_tw[74])
    print()

    print("2C. Amount of different POS tags...")
    unique_tags = set([pair[TAG] for pair in br_tw])
    print("{} different POS tags".format(len(unique_tags)))
    print()

    print("2D. Top 15 words...")
    words = [pair[WORD] for pair in br_tw]
    for word, count in Counter(words).most_common(15):
        print(count, word)
    print()

    print("2E. Top 15 POS tags...")
    tags = [pair[TAG] for pair in br_tw]
    for tag, count in Counter(tags).most_common(15):
        print(count, tag)
    print()

    print("2F. Most frequent POS tag in the 20th and the 40th sentence...")
    print(most_frequent_tag_in_sentence(br_ts[19]))
    print(most_frequent_tag_in_sentence(br_ts[39]))
    print("Note: both sentences only contain unique tags"
          " and therefore every tag has a frequency of 1.")
    print()

    print("2G. Most frequent adverb...")
    print()

    print("2H. Most frequent adjective...")
    print()

    print("2I. POS tags for 'so'...")
    print()

    print("2J. Most frequent POS tag for 'so'...")
    print()

    print("2K. Example sentences for 'so'...")
    print()

    print("2L. Most likely POS tags preceding and following 'so'...")
    print()


def amount_of_words_and_sentences():
    """
    Get the amount of words and amount of sentences.
    :return:
    """
    return len(br_tw), len(br_ts)


def most_frequent_tag_in_sentence(sentence):
    """
    Returns the most frequent POS tag found in a given sentence.
    If
    :param sentence:
    :return:
    """
    tags = [pair[TAG] for pair in sentence]
    return Counter(tags).most_common(1)


if __name__ == '__main__':
    main()
