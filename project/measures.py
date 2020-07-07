#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"

import os
from collections import Counter
from nltk.metrics import ConfusionMatrix


def scores(labels, cm):
    """
    Given a set of labels, this script calculates
    precision, recall and f-score
    :param labels:
    :param cm:
    :return:
    """
    true_positives = Counter()
    false_negatives = Counter()
    false_positives = Counter()

    for i in labels:
        for j in labels:
            if i == j:
                true_positives[i] += cm[i, j]
            else:
                false_negatives[i] += cm[i, j]
                false_positives[j] += cm[i, j]

    print("TP:", sum(true_positives.values()), true_positives)
    print("FN:", sum(false_negatives.values()), false_negatives)
    print("FP:", sum(false_positives.values()), false_positives)
    print()

    for i in sorted(labels):
        if true_positives[i] == 0:
            fscore = 0
            recall = 0
            precision = 0
        else:
            precision = true_positives[i] / float(true_positives[i] + false_positives[i])
            recall = true_positives[i] / float(true_positives[i] + false_negatives[i])
            fscore = 2 * (precision * recall) / float(precision + recall)
        print(i)
        print('f-score:', fscore)
        print('recall:', recall)
        print('precision:', precision)
        print()


def annotations(directory):
    """
    This script walks through the different directories and creates a list of
    the gold standard items and the generated items, as well as a list of
    wikipedia links, if applicable, for both. This results in four different lists.
    :param directory:
    :return:
    """
    wiki_annotated, wiki_generated = [], []
    annotated_items, generated_items = [], []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".ent"):
                input_file_path = os.path.join(root, name)
                with open(input_file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        # This takes the tag if it has a tag, otherwise adds a space to the list
                        if len(line.split()) >= 6:
                            annotated_items.append(line.split()[5])
                        else:
                            annotated_items.append(' ')
                        # This takes the wikipedia link if it has it, otherwise adds a space to the list
                        if len(line.split()) == 7:
                            wiki_annotated.append(line.split()[6])
                        else:
                            wiki_annotated.append(' ')

            if name.endswith(".out"):
                input_file_path = os.path.join(root, name)
                with open(input_file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        # This takes the tag if it has a tag, otherwise adds a space to the list
                        if len(line.split()) >= 6:
                            generated_items.append(line.split()[5])
                        else:
                            generated_items.append(' ')
                        # This takes the wikipedia link if it has it, otherwise adds a space to the list
                        if len(line.split()) == 7:
                            wiki_generated.append(line.split()[6])
                        else:
                            wiki_generated.append(' ')

    return annotated_items, generated_items, wiki_annotated, wiki_generated


def compare_wiki(wiki1, wiki2):
    """
    This script compares two different lists to each other,
    and returns the number of matches,
    as long as the list item isn't a space.
    :param wiki1:
    :param wiki2:
    :return:
    """
    return [i for i, j in zip(wiki1, wiki2) if i == j and i != ' ']


def main():
    """
    This script generates the required output.
    First it draws a confusion matrix, gives you the scores of our system,
    and lastly shows how accurate the wikification program is.
    :return:
    """
    items1, items2, wiki1, wiki2 = annotations('test')
    #print([len(x) for x in annotations('test')])
    cm = ConfusionMatrix(items1, items2)
    print(cm)

    labels_class = ["COU", "CIT", "NAT", "PER", "ORG", "ANI", "SPO", "ENT"]
    scores(labels_class, cm)

    # This checks the numbers of links generated, and the ones annotated and divides them to give us the number of links
    # we found versus the number of links we were supposed to find
    wiki_links_annotated = [elem for elem in wiki1 if elem.strip()]
    wiki_links_generated = [elem for elem in wiki2 if elem.strip()]
    print(len(wiki_links_generated) / len(wiki_links_annotated))
    # This checks of how many links we found, were exactly the same as the ones found by the golden standard
    print(len(compare_wiki(wiki1, wiki2)) / len(wiki_links_annotated))


if __name__ == '__main__':
    main()
