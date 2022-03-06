import math
import re
import time

def TD(f):
    REGEX_DAY_TYPE = r" {21}(\w{2})"
    output = {}
    symbol_matrix = {}
    for line in f:
        if line.find('#TD') > -1:
            print(f'      TD-RETURNING')
            return output, symbol_matrix

        match = re.search(REGEX_DAY_TYPE, line)
        if match:
            print(f'      TD: {match[1]}')

            # !!! # We will **slightly** break convention here
            # by having function in the same file, since data is higly related and will be combined

            timetable = WG(f)
            departures = OD(f)

            # Merge the two
            for key in timetable:
                try:
                    timetable[key]["id"] = departures[key]
                    symbol_matrix[departures[key]] = timetable[key]
                except KeyError:
                    # 0.01 =/= 24.01
                    # the 32 hour format stirkes again
                    try:
                        # Lets convert one key to 32h format
                        big_key = key
                        big_key = big_key.split('.')
                        big_key = str(int(big_key[0]) + 24) + '.' + big_key[1]
                        timetable[key]["id"] = departures[big_key]
                        symbol_matrix[departures[big_key]] = timetable[key]  # code duplication go brr
                        # print('Autofix successful')
                        # time.sleep(0.5)
                    except KeyError:
                        print('ERROR: Autofix failure: Missing departure for: ', key, timetable[key], departures)
                        time.sleep(10)
                    

            output[match[1]] = timetable

    pass


def symbol_cleaner(dirty):
    # [45mx^ -> (45, mx, True, True)
    # check for lowfloor
    symbol = None
    lowfloor = False
    exceptional = False

    if '[' in dirty:
        lowfloor = True
    
    dirty = dirty.replace('[', '')
    dirty = dirty.replace(']', '')

    if '^' in dirty:
        exceptional = True
        dirty = dirty.replace('^', '')

    # finally, symbol
    if len(dirty) > 2:
        symbol = dirty[2:]
        dirty = dirty[:2]

    return dirty, symbol, lowfloor, exceptional


def WG(f):
    REGEX_TIMETABLE = r" {27}G +\d+ +(\d+): +(.+)"  # requiers further parsing
    output = {}

    for line in f:
        if line.find('#WG') > -1:
            print(f'      WG-RETURNING')
            return output
        
        match = re.search(REGEX_TIMETABLE, line)
        if match:
            minutes = match[2]
            minutes = minutes.split()
            for min in minutes:
                clean, symbol, lowfloor, exceptional = symbol_cleaner(min)
                key = match[1] + '.' + clean
                output[key] = {
                    "symbol": symbol,
                    "lowfloor": lowfloor,
                    "exceptional": exceptional,
                }

    pass

def OD(f):
    REGEX_DEPARTURES = r" {27} ?(\d+\.\d+)  (.+)"
    output = {}

    for line in f:
        if line.find('#OD') > -1:
            print(f'      OD-RETURNING')
            return output
        
        match = re.search(REGEX_DEPARTURES, line)
        if match:
            output[match[1]] = match[2]
