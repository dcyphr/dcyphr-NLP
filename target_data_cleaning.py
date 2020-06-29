import re

filepath = "summary.txt"
with open(filepath) as fp:
    lines = fp.readlines()
    for line in lines:
        # TODO 
        # separate each new section (delimited by <h2>) into new line
        # add delimiter " | " after </h2>
        # remove html tags
        return