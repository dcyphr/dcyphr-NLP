import re
import os
import sys
import argparse
import csv

def make_file(filepath, outpath):
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
            data = row[0]
            sections = re.split('(<h2.*?>)', data) # regex to split by section
            for section in sections:
                section = section.replace('</h2>', ' | ') # replaces closing tag with delimiter
                section = re.sub(clean, '', section) # cleans section using compiled regex from above
                target = open(outpath, 'a') # opens and writes into new file
                target.write(section + ' \n')
                target.close()

def main():
    parser = argparse.ArgumentParser(
        description = 'Transforms dcyphr csv to target text file',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('src', type = str,
                        help = 'Path to input csv')
    parser.add_argument('out', type = str,
                        help = 'Path to output csv')
    
    args = parser.parse_args()

    filepath = args.src
    outpath = args.out

    if os.path.isfile(outpath):
        os.remove(outpath)
    open(outpath, 'a').close()

    make_file(filepath, outpath)

if __name__ == '__main__':
    main()
