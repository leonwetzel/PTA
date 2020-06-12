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

import nltk


def main():
    """
    You will have to run a POS tagger on your data. Please, remember that you will have
    to use the POS tagger we have seen in class, with the nltk.pos tag() NLTK function.
    When you call it, you will have to make sure to give it the right input, but then
    you will have to convert it back to the column format. It is important that after
    the fifth column is added, the format of the original file isn’t changed.

    :return:
    """
    # iterate over the files in the various directories
    for subdir, dirs, files in os.walk('group12'):
        for file in files:
            extension = os.path.splitext(file)[-1].lower()
            if '.off' in extension:
                # deduct file name and instantiate variables
                offsets_start, offsets_end = [], []
                ids, tokens = [], []
                input_file_name = os.path.join(subdir, file)

                # read lines from the offset file
                with open(input_file_name, 'r') as F:
                    token_rows = F.readlines()

                # iterate over the lines and place values in their designated variables
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

                # get the post tags
                pos_tags = nltk.pos_tag(tokens)

                # write values to new file
                output_file_name = os.path.join(subdir, 'en.tok.off.pos')
                with open(output_file_name, 'w') as F:
                    for off_start, off_end, id, pos_tag in\
                            zip(offsets_start, offsets_end, ids, pos_tags):
                        F.write(f"{off_start} {off_end} {id} {pos_tag[0]} {pos_tag[1]}\n")


if __name__ == '__main__':
    main()
