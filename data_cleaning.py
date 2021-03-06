import os
import argparse
import sys
import re
from link_parse import *
import csv
import Levenshtein

# USE THIS COMMAND TO RUN FILE: python data_cleaning.py merge.csv source.txt target.txt

# compiled regex to remove HTML tags, nbsp, style attributes, percent signs, excessive spacing, and newlines
clean = re.compile("""<.*?>|&nbsp;|style=("|').*?("|')|%|([ ]|[\t]){2,}|\r?\n|\r""")


def scrape_function(link):

    """
    Write function to scrape links and return dictionary of {section_header:section_text}
    """
    try:
        dicti = {}
        if 'lancet' in link:
            dicti = lancet(link)
        elif 'cell' in link:
            dicti = cell_extract(link)
        elif 'pubmed' in link:
            dicti = ncbi_pubmed_extract(link)
        elif 'nature' in link:
            dicti = scrape_nature(link)
        elif ('nejm' in link):
            dicti = nejm_extract(link)
        elif ('ncbi' in link):
            dicti = pmc_extract(link)
        elif ('sciencemag' in link):
            scimag(link)
        elif ('medrxiv' in link):
            medrxiv(link)
        elif 'pnas' in link:
            pnas(link)

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


def remove_space_num(s):
    s=re.sub('\W+',' ',s).strip()
    for i in range(len(s)):
        if (s[i]==" "):
            s= s[i+1:].strip()
            break
        
    return s


def write_file(sections_original, sections_target, source_file, target_file):
    """ Write file after obtaining from sections_original, sections_target and writing into
    source_file and target_file.
    """
    source = open(source_file, "a")
    target = open(target_file, "a")

    for i in sections_original.keys():
        for j in sections_target.keys():
            if i in j or j in i:
                source.write('\n')
                source.write("<NbChars_" + str(calculate_nb_chars(sections_original[i], sections_target[j])) + ">")
                source.write("<LevSim_" + str(get_levenshtein_similarity(sections_original[i], sections_target[j])) + ">")
                source.write("<"+ remove_space_num(i) +">")
                data_source = " ".join(sections_original[i].split())
                source.write(data_source)

                target.write('\n')
                # target.write(remove_space_num(i))
                data_target = " ".join(sections_target[j].split())
                target.write(data_target)


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

    


if __name__ == '__main__':
    main()