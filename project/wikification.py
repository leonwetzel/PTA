#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"

import csv
import os
from nltk.parse import CoreNLPParser
import errno


def find_files(folder, ends_with):
    page_id_list = []
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ends_with):
                page_id_list.append(os.path.join(subdir, file))
    return page_id_list


def create_tokens(file):
    with open(file) as csv_file:
        words_list = []
        reader = csv.reader(csv_file, delimiter=' ')
        for row in reader:
            words_list.append(row[3])
    return words_list


def tag_ner(file):
    ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')
    ner_tagged = (list(ner_tagger.tag((file))))
    return ner_tagged


def write_to_files(ner_dict):
    for key, value in ner_dict.items():
        filename = "ner_results/" + key
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with open('ner_results/' + key, 'w') as file:
            for combo in value:
                file.write(combo[0] + " " + combo[1] + '\n')


def main():
    words_dict = {}
    ner_dict = {}
    file_names = find_files('dev', '.pos')
    for file in file_names:
        words_dict[file] = create_tokens(file)
        ner_dict[file] = tag_ner(words_dict[file])
        write_to_files(ner_dict)
    location_finder = find_files('ner_results', '.pos')


if __name__ == '__main__':
    main()
