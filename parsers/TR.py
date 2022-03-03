import re
from .LW import LW

def TR(f):
    regex = r" {9}(\w{2}-[\w-]+)(?: +)?, +([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+), +(.{2}) +==> +([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+), +(.{2}) +Kier. (\w) +Poz. (\w)"
    output = {}
    for line in f:
        if line.find('#TR') > -1:
            print(f'  TR-RETURNING')
            return output

        match = re.search(regex, line)
        if match:
            print(f'  TR: {match[1]}')
            # key found, pass contents
            full, stops, roads_desc = LW(f)
            output[match[1]] = {
                "route_id": match[1],
                "from": match[2],
                "from_city": match[3],
                "to": match[4],
                "to_city": match[5],
                "dir": match[6],
                "index": match[7],
                "route_roads_desc": roads_desc,
                "route_stops": stops,
                "route_details": full
            }
    pass