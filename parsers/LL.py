from collections import defaultdict
import re
from .TR import TR

def LL(f):
    regex = r" {3}Linia: +([\w\-]+) +\- +(.+)"
    lines_output = {}
    timetable_output = {}
    symbols_output = {}

    # output = defaultdict(list)
    for line in f:
        if line.find('#LL') > -1:
            return lines_output, timetable_output, symbols_output
        
        match = re.search(regex, line)
        if match:
            # key found, pass contents
            print(f'LL: {match[1]}')
            routes, timetables, symbols = TR(f)
            lines_output[match[1]] = {
                "number": match[1],  # line number (1, 2, 523, N83 etc.)
                "type": match[2],  # line type (bus/tram)
                "routes": routes
            }

            timetable_output[match[1]] = timetables

            symbols_output[match[1]] = symbols

            if match[1] == '709':
                return lines_output, timetable_output, symbols_output
            