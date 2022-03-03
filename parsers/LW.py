import re


def LW(f):

    # this regex differs slightly next to group 4: it has ?, instead of ,
    regex_stop = r" {15}(?:([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+),)? +(r)? (\d+)  ([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+),? +(.{2}) (\d\d)  (NŻ)? +\| ?(\d\d?)\| ?(\d\d?)"
    regex_road = r" {15}(?:([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+),) +\|  \|  \|"

    full_output = []
    stops_output = []
    roads_output = []

    for line in f:
        if line.find('#LW') > -1:
            return full_output

        match = re.search(regex_stop, line)
        if match:
            full_output.append({
                "type": "stop",
                "road": match[1],
                "timetable_availibility": True if match[2] else False,
                "id": match[3],
                "name": match[4],
                "city": match[5],
                "num": match[6],
                "on_demand": True if match[7] else False,
                "min_time": match[8],
                "max_time": match[9]
            })

            stops_output.append(match[3])
            
        elif re.search(regex_road, line):
            match = re.search(regex_road, line)  # inefficient! (double regex matching) but since its relatively rare we let this pass
            full_output.append({
                "type": "road_change",
                "road": match[1]
            })

            roads_output.append(match[1])
    pass