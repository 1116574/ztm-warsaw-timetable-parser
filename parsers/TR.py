import re
from .LW import LW

def TR(f):
    regex = r" {9}(\w{2}-[\w-]+)(?: +)?, +([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+), +(.{2}) +==> +([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+), +(.{2}) +Kier. (\w) +Poz. (\w)"
    output = {}
    for line in f:
        if line.find('#TR') > -1:
            return output

        match = re.search(regex, line)
        if match:
            # key found, pass contents
            something = LW(f)
            output['route_id'] = match[1]
            output['from'] = match[2]
            output['from_city'] = match[3]
            output['to'] = match[4]
            output['to_city'] = match[5]
            output['dir'] = match[6]
            output['index'] = match[7]
            output['route_details'] = something
    pass