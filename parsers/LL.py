from collections import defaultdict
import re
from .TR import TR

def LL(f):
    regex = r" {3}Linia: +([\w\-]+) +\- +(.+)"
    output = {}
    output = defaultdict(list)
    for line in f:
        if line.find('#LL') > -1:
            return output
        
        match = re.search(regex, line)
        if match:
            # key found, pass contents
            something = TR(f)
            output["number"] = match[1]  # line number (1, 2, 523, N83 etc.)
            output["type"] = match[2]  # line type (bus/tram)
            output["routes"].append(something)
            

            if match[1] == '4':
                return output
            