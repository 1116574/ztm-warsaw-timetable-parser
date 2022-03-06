import re

def OP(f):
    REGEX_SYMBOLS = r" {21}S {4}(.) - (.+)"
    REGEX_COMMENT = r" {21}K {3}(.+)"
    REGEX_DATE = r" {21}D {3}(.+)"
    date = ''
    comments = []
    symbols_descriptors = {}
    for line in f:
        if line.find('#OP') > -1:
            print(f'    OP-RETURNING')
            return symbols_descriptors, comments, date

        match = re.search(REGEX_SYMBOLS, line)
        if match:
            print(f'    OP: {match[1]}')
            symbols_descriptors[match[1]] = match[2]
        elif re.search(REGEX_COMMENT, line):
            match = re.search(REGEX_COMMENT, line)
            comments.append(match[1])
        elif re.search(REGEX_DATE, line):
            match = re.search(REGEX_DATE, line)
            date = match[1]

    pass