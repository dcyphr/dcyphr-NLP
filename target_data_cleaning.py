import re
import os
import sys
import argparse
import csv

def make_file(filepath, outpath):
    clean = re.compile("""<.*?>|&nbsp;|style=("|').*?("|')|%|([ ]|[\t]){2,}|\n""")
    maxInt = sys.maxsize

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)

    with open(filepath, newline='') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=' ')
        for row in file_reader:
            data = row[0]
            sections = re.split('(<h2.*?>)', data)
            for section in sections:
                section = section.replace('</h2>', ' | ')
                section = re.sub(clean, '', section)
                target = open(outpath, 'a')
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
