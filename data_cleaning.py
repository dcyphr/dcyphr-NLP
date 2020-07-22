import os
import argparse
import sys
import re
import link_parse
# USE THIS COMMAND TO RUN FILE:  python target_data_cleaning.py summary.csv summary.txt

# compiled regex to remove HTML tags, nbsp, style attributes, percent signs, excessive spacing, and newlines
clean = re.compile("""<.*?>|&nbsp;|style=("|').*?("|')|%|([ ]|[\t]){2,}|\r?\n|\r""")
 
def scrape_function(link):
    # TODO
    """
    Write function to scrape links and return dictionary of {section_header:section_text}
    """
    if('lancet' in link):
        dicti=lancet(link)
    elif('cell' in link):
        dicti=cell_extract(link)
    elif('pubmed' in link):
        dicti=ncbi_pubmed_extract(link)
    elif('nature' in link):
        dicti=scrape_nature(link)
    return dicti


def clean_target(summary):
    sections = re.split('<h2.*?>', summary)
    output = {}
    for section in sections:
        print(section)
        if section!='':
            temp = re.split('</h2>', section)
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
            maxInt = int(maxInt/10)

    # opens csv file
   with open(filepath, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=' ')

        # for each row in csv, split up by section
        for row in file_reader:
            souce_article_link = row[0]
            target_summary = row[1]

            # TODO
            """
            Scrape from source_article_link
            Check if section scraped from links matches with sections in summary
            """

            sections_original = scrape_function(source_article_link) # outputs a dict
            sections_target = clean_target(target_summary) # outputs a dict
            


def main():
    parser = argparse.ArgumentParser(
            description = 'Transforms csv (link, summary) to source.txt and target.txt',
            formatter_class = argparse.ArgumentDefaultsHelpFormatter
            )
    parser.add_argument('src', type = str,
            help = 'Filename for input csv')
    parser.add_argument('out_source', type=str,
            help = 'Filename for output source.txt')
    parser.add_argument('out_target', type=str,
            help = 'Filename for output target.txt')
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

    print(clean_target("<h2 style=blah>Abstract</h2><p>This is some text</p><h2>Introduction</h2><span>blah blah</span>"))

if __name__ == '__main__':
    main()

