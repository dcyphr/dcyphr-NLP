import os
import sys
import re

def make_file(filepath, source_out, target_out):
    # compiled regex to remove HTML tags, nbsp, style attributes, percent signs, excessive spacing, and newlines
    clean = re.compile("""<.*?>|&nbsp;|style=("|').*?("|')|%|([ ]|[\t]){2,}|\r?\n|\r""")
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

            sections = re.split('(<h2.*?>)', target_summary) # regex to split by section
            for section in sections:
                # TODO
                """Check if section scraped from links matches with sections in summary"""
                section = section.replace('</h2>', ' | ') # replaces closing tag with delimiter 
                section = re.sub(clean, '', section) # cleans section using compiled regex from above
                target = open(target_out, 'a') # opens and writes into new file
                target.write(section + ' \n')
                target.close()


