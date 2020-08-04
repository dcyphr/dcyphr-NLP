import os
import argparse
import sys
import re
from link_parse import *
import csv
import Levenshtein

# USE THIS COMMAND TO RUN FILE:  python target_data_cleaning.py summary.csv summary.txt

# compiled regex to remove HTML tags, nbsp, style attributes, percent signs, excessive spacing, and newlines
clean = re.compile("""<.*?>|&nbsp;|style=("|').*?("|')|%|([ ]|[\t]){2,}|\r?\n|\r""")


def scrape_function(link):
    # TODO
    """
    Write function to scrape links and return dictionary of {section_header:section_text}
    """
    try:
        dicti = {}
        if 'lancet' in link:
            print('lancet')
            dicti = lancet(link)
        elif 'cell' in link:
            print('cell')
            dicti = cell_extract(link)
        elif 'pubmed' in link:
            print('pubmed')
            dicti = ncbi_pubmed_extract(link)
        elif 'nature' in link:
            print('nature')
            dicti = scrape_nature(link)
        elif ('nejm' in link):
            print('nejm')
            dicti = nejm_extract(link)
        elif ('ncbi' in link):
            print('pmc')
            dicti = pmc_extract(link)
        elif ('sciencemag' in link):
            print('scimag')
            scimag(link)
        elif ('medrxiv' in link):
            print('medrxiv')
            medrxiv(link)
        elif 'pnas' in link:
            print('pnas')
            pnas(link)
        else:
            print('other', link)
    except:
        print(link)
    return dicti


def clean_target(summary):
    sections = re.split('<h2.*?>', summary)
    output = {}

    for section in sections:
        if section != '':

            temp = re.split('</h2>', section)
            if (len(temp) <= 1):
                continue
            section_heading = re.sub(clean, '', temp[0])
            section_text = re.sub(clean, '', temp[1])
            output[section_heading] = section_text
    return output


def make_file(filepath, source_out, target_out):
    maxInt = sys.maxsize

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    # opens csv file
    with open(filepath, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',')

        # for each row in csv, split up by section
        for row in file_reader:
            souce_article_link = row[0]
            target_summary = row[1]
            # TODO
            """
            Scrape from source_article_link
            Check if section scraped from links matches with sections in summary
            """

            sections_original = scrape_function(row[0])  # outputs a dict
            sections_target = clean_target(row[1])  # outputs a dict
            if ('References' in sections_original):
                del sections_original['References']
            write_file(sections_original, sections_target, source_out, target_out)


def write_file(sections_original, sections_target, source_file, target_file):
    f = open(source_file, "a")
    s = open(target_file, "a")

    for i in sections_original.keys():
        for j in sections_target.keys():
            if i in j or j in i:
                f.write('\n')
                f.write("<NbChars_" + str(calculate_nb_chars(sections_original[i], sections_target[j])) + ">")
                f.write("<LevSim_" + str(get_levenshtein_similarity(sections_original[i], sections_target[j])) + ">")
                f.write(i + '|')
                m = " ".join(sections_original[i].split())
                f.write(m)

                s.write('\n')
                s.write(i + '|')
                n = " ".join(sections_target[j].split())
                s.write(n)


def calculate_nb_chars(original_sentence, simple_sentence):
    """Calculate and return the character length ratio between an original sentence 
    and a simplified sentence"""
    return round(len(simple_sentence) / len(original_sentence), 1)


def get_levenshtein_similarity(complex_sentence, simple_sentence):
    """ Return the similarity between complex_sentence and simple_sentence """
    return round(Levenshtein.ratio(complex_sentence, simple_sentence), 1)


def main():
    parser = argparse.ArgumentParser(
        description='Transforms csv (link, summary) to source.txt and target.txt',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('src', type=str,
                        help='Filename for input csv')
    parser.add_argument('out_source', type=str,
                        help='Filename for output source.txt')
    parser.add_argument('out_target', type=str,
                        help='Filename for output target.txt')
    args = parser.parse_args()

    input_file = args.src
    output_source = args.out_source
    output_target = args.out_target

    if os.path.isfile(output_source):
        os.remove(output_source)
    if os.path.isfile(output_target):
        os.remove(output_target)
    open(output_source, 'a').close()
    open(output_target, 'a').close()

    make_file(input_file, output_source, output_target)

    print(
        clean_target("<h2 style=blah>Abstract</h2><p>This is some text</p><h2>Introduction</h2><span>blah blah</span>"))


if __name__ == '__main__':
    main()