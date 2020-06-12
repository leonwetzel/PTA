#!/usr/bin/python3
__author__ = "Leon Wetzel, Teun Buijse and Roman Terpstra"
__copyright__ = "Copyright 2020 - Leon Wetzel, Teun Buijse and Roman Terpstra"
__credits__ = ["Leon Wetzel", "Teun Buijse", "Roman Terpstra"]
__license__ = "GPL"
__version__ = "0.1"
__email__ = ["l.f.a.wetzel@student.rug.nl", "t.c.buijse@student.rug.nl",
             "r.p.terpstra@student.rug.nl"]
__status__ = "Development"

import os
import re

import spacy

nlp = spacy.load("entity_tagger")


def find_files(folder, ends_with):
    page_id_list = []
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ends_with):
                page_id_list.append(os.path.join(subdir, file))
    return page_id_list


# def create_tokens(file):
#     with open(file) as csv_file:
#         words_list = []
#         reader = csv.reader(csv_file, delimiter=' ')
#         for row in reader:
#             words_list.append(row[3])
#     return words_list


def tag_ner(char_offset_starts, char_offset_ends, ids, tokens, pos_tags):
    """
    Tags named entities.

    :param char_offset_starts:
    :param char_offset_ends:
    :param ids:
    :param tokens:
    :param pos_tags:
    :return:
    """
    """
    :param char_offset_starts: 
    :param char_offset_ends: 
    :param ids: 
    :param tokens: 
    :param pos_tags: 
    :return: 
    """
    sentence = re.sub(r'\s([?.,!"](?:\s|$))', r'\1', " ".join(tokens))
    doc = nlp(sentence)
    entities, ner_tagged, ners = [], [], []

    for entity in doc.ents:
        entities.append({
            "text": entity.text,
            "label": entity.label_,
            "start": entity.start_char,
            "end": entity.end_char,
        })
        ners.append(entity.text)

    for index, token in enumerate(tokens):
        if token in ners:
            entity = next(ent for ent in entities if ent['text'] == token)
            ner_tagged.append(f"{entity['start']} {entity['end']}"
                              f" {ids[index]} {token} {pos_tags[index]} {entity['label']}")
        else:
            ner_tagged.append(f"{char_offset_starts[index]} {char_offset_ends[index]}"
                              f" {ids[index]} {token} {pos_tags[index]}")

    return ner_tagged


def main():
    """
    sadsadsadsad
    :return:
    """
    extension = ".pos" # .ent

    for subdir, dirs, files in os.walk("dev"):
        for file in files:
            if file.endswith(extension):
                # instantiate variables
                offsets_start, offsets_end, ners = [], [], []
                ids, tokens, pos_tags, urls = [], [], [], []
                input_file_name = os.path.join(subdir, file)

                # read lines from the offset file
                with open(input_file_name, 'r') as F:
                    token_rows = F.readlines()

                # iterate over the lines and place values in their designated variables
                for row in token_rows:
                    column_count = len(row.strip().split())
                    if column_count == 7:
                        # annotated row
                        char_offset_start, char_offset_end, id, token, pos_tag, ner, wikipedia_link = row.strip().split()
                        ners.append(ner)
                        urls.append(wikipedia_link)
                    elif column_count == 5:
                        # row does not contain annotated information
                        char_offset_start, char_offset_end, id, token, pos_tag = row.strip().split()
                    elif column_count == 6:
                        # a faulty length, but we can handle that...
                        char_offset_start, char_offset_end, id, token, pos_tag, ner = row.strip().split()
                    else:
                        # row does not comply with standards, skip it
                        continue

                    offsets_start.append(char_offset_start)
                    offsets_end.append(char_offset_end)
                    ids.append(id)
                    tokens.append(token)
                    pos_tags.append(pos_tag)

                output = tag_ner(offsets_start, offsets_end, ids, tokens, pos_tags)

                output_file_name = os.path.join(subdir, 'en.tok.off.pos.ent.out')
                with open(output_file_name, 'w') as F:
                     for row in output:
                        F.write(f"{row}\n")


if __name__ == '__main__':
    main()
