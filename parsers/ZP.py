import re
from .PR import PR

def ZP(f):
    REGEX = r" {3}(\d{4}) {3}(\S+) +(.{2})  (.+)"
    output = {}
    # output = defaultdict(list)
    for line in f:
        if line.find('#ZP') > -1:
            return output
        
        match = re.search(REGEX, line)
        if match:
            # key found, pass contents
            print(f'ZP: {match[1]}')
            something = PR(f)
            output[match[1]] = {
                "id": match[1],
                "name": match[2],
                "city_id": match[3],
                "city": match[4]
            }

            output[match[1]].update(something)
