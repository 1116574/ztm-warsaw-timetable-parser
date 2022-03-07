import re
from collections import defaultdict


def WK(f):
    REGEX = r" {9}(.+)  (\d+) (.{2}) +(\d+\.\d+)  (.)?"
    output = defaultdict(list)

    for line in f:
        if line.find('#WK') > -1:
            print(f'  WK-RETURNING')
            return output

        match = re.search(REGEX, line)
        if match:
            print(f'  WK: {match[1]}')
            output[match[1]].append([match[2], match[4], match[5]])
            
            # "trip_id": match[1],
            # "stop_id": match[2],
            # "day": match[3],
            # "time": match[4],
            # "flag": match[5],

    pass