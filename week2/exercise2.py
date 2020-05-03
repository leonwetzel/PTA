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

br_tw = nltk.corpus.brown.tagged_words(categories='mystery', tagset='brown')
br_ts = nltk.corpus.brown.tagged_sents(categories='mystery', tagset='brown')
tagset = nltk.load('help/tagsets/brown_tagset.pickle')
WORD, TAG = 0, 1


def main():
    """
    Performs assignment 2.
    """
    print("ASSIGNMENT 2 - PART 2")
    print("==============================================\n")

    amount_of_words, amount_of_sentences = amount_of_words_and_sentences()
    print("2A. Amount of words and sentences...")
    print("- words: {}".format(amount_of_words))
    print("- sentences: {}".format(amount_of_sentences))
    print()

    print("2B. 50th and 75th words and tags...")
    for index in {49, 74}:
        print("{}: {} ({})".format(br_tw[index][WORD],
                                   br_tw[index][TAG],
                                   tagset[br_tw[index][TAG]][0]))
    print()

    print("2C. Amount of different POS tags...")
    unique_tags = {pair[TAG] for pair in br_tw}
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
        print("{}: {} ({})".format(count, tag, tagset[tag][0]))
    print()

    print("2F. Most frequent POS tag in the 20th and the 40th sentence...")
    pos_tag, count = most_frequent_tag_in_sentence(br_ts[19])
    print("{}: {} ({})".format(count, pos_tag, tagset[pos_tag][0]))
    pos_tag, count = most_frequent_tag_in_sentence(br_ts[39])
    print("{}: {} ({})".format(count, pos_tag, tagset[pos_tag][0]))
    print("Note: both sentences only contain unique tags"
          " and therefore every tag has a frequency of 1.\n"
          "The returned values are returned based on alphabetical order.")
    print()

    print("2G. Most frequent adverb...")
    print("Note: the set of adverbs is based on"
          " https://en.wikipedia.org/wiki/Brown_Corpus")
    adverbs = {"RB", "RBR", "RBT", "RN", "RP"}
    adverbs_in_corpus = [pair[WORD] for pair in br_tw if pair[TAG] in adverbs]
    most_frequent_adverb, count = Counter(adverbs_in_corpus).most_common(1)[0]
    print("{} ({} occurences)".format(most_frequent_adverb, count))
    print()

    print("2H. Most frequent adjective...")
    print("Note: the set of adjectives is based on"
          " https://en.wikipedia.org/wiki/Brown_Corpus")
    adjectives = {"JJ", "JJR", "JJS", "JJT"}
    adjectives_in_corpus = [pair[WORD] for pair in br_tw if pair[TAG] in adjectives]
    most_frequent_adjective, count = Counter(adjectives_in_corpus).most_common(1)[0]
    print("{} ({} occurences)".format(most_frequent_adjective, count))
    print()

    print("2I. POS tags for 'so'...")
    unique_so_tags = {pair[TAG] for pair in br_tw if pair[WORD] == 'so'}
    for tag in unique_so_tags:
        print("{} ({})".format(tag, tagset[tag][0]))
    print()

    print("2J. Most frequent POS tag for 'so'...")
    so_tags = [pair[TAG] for pair in br_tw if pair[WORD] == 'so']
    most_frequent_so_pos_tag, count = Counter(so_tags).most_common(1)[0]
    print("{} - {} ({} occurences)".format(most_frequent_so_pos_tag,
                                           tagset[most_frequent_so_pos_tag][0], count))
    print()

    print("2K. Example sentences for 'so'...")
    queue = unique_so_tags.copy()
    for sentence in br_ts:
        for pair in sentence:
            if 'so' == pair[WORD] and pair[TAG] in queue:
                queue.remove(pair[TAG])
                output = [pair[WORD] for pair in sentence]
                print("{} ({}):".format(pair[TAG], tagset[pair[TAG]][0]),
                      " ".join(output))
    print()

    print("2L. Most likely POS tags preceding and following 'so'...")
    preceding_tags, following_tags = [], []
    for sentence in br_ts:
        for index, pair in enumerate(sentence):
            if pair[WORD] == 'so':
                previous_pair = sentence[index - 1]
                preceding_tags.append(previous_pair[TAG])
                next_pair = sentence[index + 1]
                following_tags.append(next_pair[TAG])

    most_likely_pair_preceding_so = Counter(preceding_tags).most_common(1)[0]
    print("Most likely POS tag preceding 'so': {} ({})".format(
        most_likely_pair_preceding_so[0], tagset[most_likely_pair_preceding_so[0]][0])
    )

    most_likely_pair_following_so = Counter(following_tags).most_common(1)[0]
    print("Most likely POS tag following 'so': {} ({})".format(
        most_likely_pair_following_so[0], tagset[most_likely_pair_following_so[0]][0])
    )
    print()

    print("==============================================")
    print("ASSIGNMENT 2 - PART 3")
    print("==============================================\n")

    """
    What if our text isn’t tagged for parts-of-speech yet? We can do it ourselves! There is a
    function in nltk, namely nltk.pos tag(), that will let you do that. Remember that
    first you will have to tokenise your data. Write a few lines that will pos-tag the whole
    of holmes.txt.
    """

    print("==============================================")
    print("ASSIGNMENT 2 - PART 4")
    print("==============================================\n")

    """
    Get collocations for POS tags, choosing whether you want to use PMI or chi-squared,
    and rank the top 5 significant bigrams you get out (your script should specify this,
    and your report too). Please, answer these questions:
    • do they look interesting at all?
    • do they differ from the top 5 POS bigrams ordered by raw frequencies?
    • what could they be used for?
    """


def amount_of_words_and_sentences():
    """
    Get the amount of words and amount of sentences.
    :return: amount of words and amount of sentences
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
    return Counter(tags).most_common(1)[0]


if __name__ == '__main__':
    main()
