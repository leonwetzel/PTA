#!/usr/bin/python3
from __future__ import unicode_literals, print_function

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
import plac
import random
import warnings
from pathlib import Path

import spacy
from spacy.util import minibatch, compounding

import pdb

LABELS = {"COU", "CIT", "NAT", "PER", "ORG", "ANI", "SPO", "ENT"}


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=r"C:\Users\leonw\Documents\PTA\project\beun", n_iter=100):
    """
    Load the model, set up the pipeline and train the entity recognizer.
    """
    nlp = spacy.blank("en")  # create blank Language class
    print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    reset_weights = False
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
        reset_weights = True
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    train_data = convert_train_data()

    print(train_data)

    # add labels
    for _, annotations in train_data:
        for ent in LABELS: #  annotations.get("entities"):
            ner.add_label(ent)

        # get names of other pipes to disable them during training
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        # only train NER
        with nlp.disable_pipes(*other_pipes) and warnings.catch_warnings():
            # show warnings for misaligned entity spans once
            warnings.filterwarnings("once", category=UserWarning, module='spacy')

            # reset and initialize the weights randomly – but only if we're
            # training a new model
            if model is None:
                nlp.begin_training()
            for itn in range(n_iter):
                random.shuffle(train_data)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        losses=losses
                    )

                print("Losses", losses)

        # test the trained model
        for text, _ in train_data:
            doc = nlp(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

        # save model to output directory
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            nlp.to_disk(output_dir)
            print("Saved model to", output_dir)

            # test the saved model
            print("Loading from", output_dir)
            nlp2 = spacy.load(output_dir)
            for text, _ in train_data:
                doc = nlp2(text)
                print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
                print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


def convert_train_data():
    train_data = []
    for subdir, dirs, files in os.walk(r'C:\Users\leonw\Documents\PTA\project\dev'):
        for file in files:
            extension = os.path.splitext(file)[-1].lower()
            if '.ent' in extension:
                # deduct file name and instantiate variables
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
                        char_offset_start, char_offset_end, id, token, pos_tag, ner, wikipedia_link = row.strip().split()
                        ners.append(ner)
                        urls.append(wikipedia_link)
                    elif column_count == 5:
                        char_offset_start, char_offset_end, id, token, pos_tag = row.strip().split()
                        ners.append("UNK")
                        urls.append("404")
                    else:
                        # row does not comply with standards
                        continue

                    offsets_start.append(char_offset_start)
                    offsets_end.append(char_offset_end)
                    ids.append(id)
                    tokens.append(token)
                    pos_tags.append(pos_tag)

                output_string = re.sub(r'\s([?.,!"](?:\s|$))', r'\1', " ".join(tokens))
                entities_details = []

                for token, named_entity in zip(tokens, ners):
                    if named_entity != 'UNK' and token:
                        results = [(m.start(0), m.end(0)) for m in re.finditer(rf"\b{token}\b", output_string)]

                        for result in results:
                            entities_details.append((result[0],
                                                    result[1],
                                                    named_entity))
                entities_details = sorted(list(set(entities_details)))

                for index, entity in enumerate(entities_details):
                    if entities_details[index][0] == entities_details[index-1][0] or\
                            entities_details[index][1] == entities_details[index-1][1]:
                        entities_details.remove(entities_details[index])

                train_data.append((
                    output_string,
                    {"entities": entities_details}
                ))

    return train_data


if __name__ == '__main__':
    plac.call(main)
