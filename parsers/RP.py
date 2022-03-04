import re
from .TD import TD

def RP(f):
    regex = r" {15}(\d{6})"  # I could parse the whole line, but why? ITs data is already in ZP
    output = {}
    symbols_output = {}
    for line in f:
        if line.find('#RP') > -1:
            print(f'    RP-RETURNING')
            return output, symbols_output

        match = re.search(regex, line)
        if match:
            print(f'    RP: {match[1]}')
            result, symbols = TD(f)  # {DP, SB, ND ...}
            output[match[1]] = {
                "id": match[1],
                "deparures": result
            }

            symbols_output[match[1]] = symbols

            # now to *TD
    pass