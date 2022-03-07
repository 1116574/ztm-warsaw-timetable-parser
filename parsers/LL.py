from collections import defaultdict
import re

from .WK import WK
from .TR import TR

def LL(f, parse_stop_times=True, parse_symbols=True, parse_timetables=True, parse_routes=True):
    regex = r" {3}Linia: +([\w\-]+) +\- +(.+)"
    lines_output = {}
    timetable_output = {}
    symbols_output = {}
    stop_times = {}

    # output = defaultdict(list)
    for line in f:
        if line.find('#LL') > -1:
            return lines_output, timetable_output, symbols_output
        
        match = re.search(regex, line)
        if match:
            # key found, pass contents
            print(f'LL: {match[1]}')
            if parse_routes:
                routes, timetables, symbols = TR(f)
                lines_output[match[1]] = {
                    "number": match[1],  # line number (1, 2, 523, N83 etc.)
                    "type": match[2],  # line type (bus/tram)
                    "routes": routes
                }

            if parse_timetables:
                timetable_output[match[1]] = timetables

            if parse_symbols:
                symbols_output[match[1]] = symbols

            if parse_stop_times:
                stop_times[match[1]] = WK(f)

            if match[1] == '103':
                return lines_output, timetable_output, symbols_output, stop_times
            