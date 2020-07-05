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
import re

import spacy
import wikipedia

wikipedia.set_lang("en")
nlp = spacy.load("entity_tagger")


def main():
    """
    Loads data from a directory, detects named entities
    and assigns a Wikipedia link to these named entities
    if possible and available.
    :return:
    """
    extension = ".pos" # .ent

    for subdir, dirs, files in os.walk("test"):
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


def import_spacy_info(doc):
    """
    Extracts NER information from the spaCy objects
    and stores them in lists, so that we can use the
    information in a later phase.

    spaCy objects are lazily stored, hence why we need
    to save the information ourselves!
    :param doc:
    :return:
    """
    entities, ners = [], []
    for entity in doc.ents:
        entities.append({
            "text": entity.text,
            "label": entity.label_,
            "start": entity.start_char,
            "end": entity.end_char,
        })
        ners.append(entity.text)
    return entities, ners


def discover_named_entity_combos(entities):
    """
    Given a set of entities, this script tries to
    find combination of named entities based on start and
    end positions of the tokens.
    :param entities:
    :return:
    """
    named_entities, combination = [], []
    for index, entity in enumerate(entities):
        if index < 1:
            combination.append(entity['text'])
            continue

        current_start = entity['start']
        previous_end = entities[index - 1]['end']

        if int(previous_end + 1) == current_start:
            # potential pair of named entities
            combination.append(entity['text'])
        else:
            # current entity does not belong to currently active pair
            # the current pair will be added to the NE stack
            named_entities.append(combination.copy())
            combination.clear()
            combination.append(entity['text'])
    return named_entities


def extract_named_entities(tokens):
    """
    Extracts named entities using our sophisticated model.
    Returns these named entities in several lists and a dictionary,
    for later usage in the application.
    :param sentence:
    :return:
    """
    sentence = re.sub(r'\s([?.,!"](?:\s|$))', r'\1', " ".join(tokens))
    doc = nlp(sentence)
    entities, ners = import_spacy_info(doc)
    entities = sorted(entities, key=lambda k: k['start'])
    named_entities = discover_named_entity_combos(entities)
    return ners, entities, named_entities


def find_wikipedia_link(query):
    """
    Tries to find the right Wikipedia
    link for a given term.
    :param query:
    :return:
    """
    try:
        page = wikipedia.page(query, auto_suggest=True).url
    except wikipedia.exceptions.DisambiguationError as e:
        page = wikipedia.page(e.options[0], auto_suggest=True).url
    except wikipedia.exceptions.PageError:
        page = None
    except:
        page = None
    return page


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
    plain_named_entities, entities, named_entities = extract_named_entities(tokens)
    tagged_named_entities = []

    for index, token in enumerate(tokens):
        # wikipedia links are only relevant
        # for named entities in our case
        if token in plain_named_entities:
            page = None

            for ne_combination in named_entities:
                if token in ne_combination:
                    query = ' '.join(ne_combination)
                    try:
                        page = find_wikipedia_link(query)
                    except:
                        page = None

            entity = next(ent for ent in entities if ent['text'] == token)

            if page:
                tagged_named_entities.append(f"{entity['start']} {entity['end']}"
                                  f" {ids[index]} {token} {pos_tags[index]} {entity['label']} {page}")
            else:
                tagged_named_entities.append(f"{entity['start']} {entity['end']}"
                                  f" {ids[index]} {token} {pos_tags[index]} {entity['label']}")
        else:
            tagged_named_entities.append(f"{char_offset_starts[index]} {char_offset_ends[index]}"
                              f" {ids[index]} {token} {pos_tags[index]}")
    return tagged_named_entities


if __name__ == '__main__':
    main()
