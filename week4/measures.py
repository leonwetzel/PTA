import os
from collections import Counter
from nltk.metrics import ConfusionMatrix

ref  = 'DET NN VB DET JJ NN NN IN DET NN'.split()
tagged = 'DET VB VB DET NN NN NN IN DET NN'.split()
cm = ConfusionMatrix(ref, tagged)


def main():
    print(cm)

    labels = set('DET NN VB IN JJ'.split())

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
        else:
            precision = true_positives[i] / float(true_positives[i] + false_positives[i])
            recall = true_positives[i] / float(true_positives[i] + false_negatives[i])
            fscore = 2 * (precision * recall) / float(precision + recall)
        print(i, fscore)


def convert():
    """
    Loads annotations from directory
    and stores them into a dictionary
    :return:
    """
    annotations = {}

    for subdir, dirs, files in os.walk('annotations'):
        for file in files:
            extension = os.path.splitext(file)[-1].lower()
            if '.pos' in extension:
                input_file_name = os.path.join(subdir, file)
                annotator = input_file_name.split('\\')[1]
                dir_name = input_file_name.split('\\')[2:4]

                # read lines from the offset file
                with open(input_file_name, 'r') as F:
                    token_rows = F.readlines()

                for row in token_rows:
                    row_data = row.split()

                    if row_data:
                        key = f"{annotator}/{dir_name[0]}/{dir_name[1]}/{row_data[2]}"
                        value = {
                            "token": row_data[3],
                            "pos_tag": row_data[4]
                        }

                        if len(row_data) > 5:
                            try:
                                value['named_entity'] = row_data[5]
                                value['wikipedia_url'] = row_data[6]
                            except IndexError:
                                value['named_entity'] = row_data[5]

                        annotations[key] = value

    for key, value in annotations.items():
        print(key, value)


def agreement_for_interest():
    pass


if __name__ == '__main__':
    convert()
