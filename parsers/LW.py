import re


def LW(f):

    # this regex differs slightly next to group 4: it has ?, instead of ,
    REGEX_STOP = r" {15}(?:([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+),)? +(r)? (\d+)  ([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+),? +(.{2}) (\d\d)  (NŻ)? +\| ?(\d\d?)\| ?(\d\d?)"
    REGEX_ROAD = r" {15}(?:([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+),) +\|  \|  \|"

    REGEX_DETOUR_BEGIN = r" {15}~~~~~~~? (początek objazdu)"
    REGEX_DETOUR_END = r" {15}~~~~~~~? (koniec objazdu)"

    REGEX_ZONE = r" {15}=+((?: PRZYSTANEK GRANICZNY )|(?:.+(\d).+))=+ +\|  \|  \|"

    ROUTE_STOP_EXPRESS_SHORTENED = r" {15}~~~~~~~? (TRASA SKRÓCONA|KURS SKRÓCONY)"

    REGEX_NEW_ROUTE_BEGIN = r" {23}(<<NOWA TRASA>>)"
    REGEX_NEW_ROUTE_END = r" {23}(<<KONIEC NOWEJ TRASY>>)"

    full_output = []
    stops_output = []
    roads_output = []
    route_type = 'normal'  # normal | shortened

    def road_change(name):
        roads_output.append(name)
        return {
            "type": "road_change",
            "road": name
        }

    def zone_change(zone):
        if zone == None:
            zone = '1/2'

        return {
            "type": "zone_change",
            "zone": zone
        }

    for line in f:
        if line.find('#LW') > -1:
            # roads_output = ' - '.join(roads_output)
            return full_output, stops_output, roads_output, route_type

        match = re.search(REGEX_STOP, line)  # Stop
        if match:
            # print(f'    LW: {match[3]}')
            if match[1]:
                full_output.append(road_change(match[1]))

            full_output.append({
                "type": "stop",
                "timetable_availibility": True if match[2] else False,
                "id": match[3],
                # "name": match[4],  # cross reference with stops.json
                # "city": match[5],  # cross reference with stops.json
                # "num": match[6],  # included in id
                "on_demand": True if match[7] else False,
                "min_time": match[8],
                "max_time": match[9]
            })

            stops_output.append(match[3])

            continue
            
        match = re.search(REGEX_ROAD, line)
        if match:
            full_output.append(road_change(match[1]))
            continue
    
        match = re.search(REGEX_ZONE, line)
        if match:
            full_output.append(zone_change(match[2]))
            continue

        match = re.search(REGEX_DETOUR_BEGIN, line)
        if match:
            full_output.append({
                "type": "detour_begin"
            })
            continue


        match = re.search(REGEX_DETOUR_END, line)
        if match:
            full_output.append({
                "type": "detour_end"
            })
            continue
        
        match = re.search(ROUTE_STOP_EXPRESS_SHORTENED, line)
        if match:
            route_type = 'shortened'
            continue

        match = re.search(REGEX_NEW_ROUTE_BEGIN, line)
        if match:
            full_output.append({
                "type": "new_route_begin"
            })
            continue

        match = re.search(REGEX_NEW_ROUTE_END, line)
        if match:
            full_output.append({
                "type": "new_route_end"
            })
            continue
    pass