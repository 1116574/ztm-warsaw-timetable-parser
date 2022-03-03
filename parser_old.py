import re
import time
import os
import json

# TODO: improve performance by detecting appropriate markers in file
# TODO: include <<NOWA TRASA>> (new route) in stop exceptions parsing
# KURS SKRÓCONY - taki który kończy trasę na wcześniejszym przystanku
# TRASA SKRÓCONA - to to samo?

AUX_PARSNG = True

# Routes
ROUTE_INFO_REGEX = r" {9}(\w{2}-[\w-]+)(?: +)?, +([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+), +(.{2}) +==> +([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+), +(.{2}) +Kier. (\w) +Poz. (\w)"
ROUTE_NAME_REGEX = r" {3}Linia: +([\w\-]+) +\- +(.+)"

# Stops on routes descriptors
STOP_REGEX = r" {15}(?:([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+),)? +(r)? (\d+)  ([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+), +(.{2}) (\d\d)  (NŻ)? +\| ?(\d\d?)\| ?(\d\d?)"
NEW_ROAD = r" {15}(?:([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+),) +\|  \|  \|"

STOP_DETOUR_REGEX = r" {15}~~~~~~~? (początek objazdu|koniec objazdu)"
STOP_ZONE_REGEX = r" {15}=+((?: PRZYSTANEK GRANICZNY )|(?:.+(\d).+))=+ +\|  \|  \|"

ROUTE_STOP_EXPRESS_SHORTENED = r" {15}~~~~~~~? (TRASA SKRÓCONA|KURS SKRÓCONY)"
NEW_ROUTE_REGEX = r" {23}(<<NOWA TRASA>>|<<KONIEC NOWEJ TRASY>>)"

# Stops on routes timetables
TIMETABLE_STOP_NAME = r" {15}(\d{6})  ([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+)[ ,]+([\w-]{2}) +Y= ([\d\.xy]+) +X= ([\d\.xy]+) +Pu=(\d)"
TIMETABLE_HUMAN = r" +G +\d+ +(\d+):(.+)"
TIMETABLE_DEPARTURES = r" +(\d+\.\d\d) +(.+)"
TIMETABLE_LEGEND = r" {21}(\w)   (.+)"

# Output JSON
JSON_OUT = {}

def parse_route_info(f):
    line_num = None
    zone_symbol = 1
    detour_symbol = '  '
    new_route_symbol = ''

    old_line_num = '1'

    section_LL = False
    section_LW = False
    section_RP = False
    section_TD = False
    section_OP = False

    section_WG = False
    section_OD = False

    stop_RP = False

    current_file = None

    stop_json = None
    stop_json_id = None

    for line in f:
        # Optimize for section headers (*RP #RP, *LW *LW)
        if line.find('*LL') > -1:
            section_LL = True
        elif line.find('#LL') > -1:
            section_LL = False

        if line.find('*LW') > -1:
            section_LW = True
        elif line.find('#LW') > -1:
            section_LW = False

        if line.find('*RP') > -1:
            section_RP = True
            index = 0  # used to count stops on route in filenames
        elif line.find('#RP') > -1:
            section_RP = False

        if line.find('*TD') > -1:
            section_TD = True
        elif line.find('#TD') > -1:
            section_TD = False

        if line.find('*OP') > -1:
            section_OP = True
        elif line.find('#OP') > -1:
            section_OP = False

        if line.find('*WG') > -1:
            section_WG = True
        elif line.find('#WG') > -1:
            section_WG = False

        if line.find('*OD') > -1:
            section_OD = True
        elif line.find('#OD') > -1:
            section_OD = False

        ### Scan over all lines
        if section_LL:
            # Line number and character (express, normal, tram, bus etc.)
            line_name = re.search(ROUTE_NAME_REGEX, line)
            if line_name:
                line_num = line_name[1]
                line_desc = line_name[2]
                #if line_name == 'L-4':
                #    time.sleep(3000)

                # If line number changes, save everything from previous one
                if old_line_num != line_num:
                    JSON_OUT[old_line_num] = line_meta
                    # with open(f'lines/{old_line_num}/index.json', 'w') as t:
                    #     json.dump(line_meta, t, indent=4)
                
                old_line_num = line_num
                
                # Folder for routes on that line
                # os.mkdir('lines/' + line_num)
                line_meta = {
                    'desc': line_desc
                }

                JSON_OUT[old_line_num] = line_meta

                # if whole line runs inside zone 1, its zone is implied and not written. Hence we need to reset it here
                zone_symbol = 1

                # reset new route flag from previous route
                new_route_symbol = ''

            # One route in line
            route = re.search(ROUTE_INFO_REGEX, line)
            if route:
                route_mem = route
                print(line_num, line_desc, route[1], route[2], route[3], route[4], route[5], route[6], route[7])

                # Reset route's data
                new_route_symbol = ''
                new_route_flag = False

                detour_symbol = '  '
                detour_flag = False

                # Folder for stops on that route
                # os.mkdir('lines/' + line_num + '/' + route[1])
                line_meta[route[1]] = {
                    'from': route[2],
                    'from_city': route[3],
                    'to': route[4],
                    'to_city': route[5],
                    'direction': route[6],
                    'variant': route[7],
                    'express_shortened': False,
                    'stops': []
                }

            # Express or shortened route (as in: line is normal in character, but this **route** is express)
            express_shortened = re.search(ROUTE_STOP_EXPRESS_SHORTENED, line)
            if express_shortened:
                print('>>', express_shortened[1])
                line_meta[route_mem[1]]['express_shortened'] = express_shortened[1]


        ### Here begins per-stop checks
        if section_LW:
            # Zone change
            zone = re.search(STOP_ZONE_REGEX, line)
            if zone:
                if zone[1].startswith(' PRZY'): 
                    # border stop; Next stop will have a new zone set so we can safely set it here to non-number
                    zone_symbol = 'X'
                else:
                    zone_symbol = zone[2]

            # Detour
            detour_express = re.search(STOP_DETOUR_REGEX, line)
            if detour_express:
                if detour_express[1] == 'początek objazdu':  # Detour start
                    detour_symbol = '; '
                    detour_flag = True
                elif detour_express[1] == 'koniec objazdu':  # Detour end
                    detour_symbol = '  '
                    detour_flag = False

            # New route
            new_route = re.search(NEW_ROUTE_REGEX, line)
            if new_route:
                if new_route[1] == '<<NOWA TRASA>>':
                    new_route_symbol = '!'
                    new_route_flag = True
                else:
                    new_route_symbol = ''
                    new_route_flag = False

            # One stop in route
            stop = re.search(STOP_REGEX, line)
            if stop:
                print(detour_symbol, zone_symbol, stop[2], stop[3], stop[4], '\t\t\t', new_route_symbol) 
                if stop[7] == 'NŻ':
                    on_demand = True
                else:
                    on_demand = False

                # TODO: Save time to get to given stop? (already parsed under stop[8] - min and stop[9] - max)
                stop_point = {
                    'id': stop[3],
                    'name': stop[4],
                    'on_demand': on_demand,
                    'zone': zone_symbol,
                    'street': stop[1],
                    'new_route': new_route_flag,
                    'detour': detour_flag,
                    'min_time': stop[8],
                    'max_time': stop[9]
                }
                # line_meta[route_mem[1]]['stops'].append([zone_symbol, stop[3], stop[4]])
                line_meta[route_mem[1]]['stops'].append(stop_point)

            # If its not a stop, maybe its only info about new road
            road = re.search(NEW_ROAD, line)
            if road:
                line_meta[route_mem[1]]['stops'].append({'street': road[1]})

        ### Every stop on route
        if section_RP and AUX_PARSNG:
            stop_timetable = re.search(TIMETABLE_STOP_NAME, line)
            if stop_timetable:
                # If one already open, close it
                # if current_file:
                #     json.dump(stop_json, current_file, indent=4)
                #     current_file.close()
                #     current_file = None  # files after closing are still fp objects
                
                # index += 1
                # current_file = open('lines/' + line_num + '/' + route_mem[1] + '/' + str(index).zfill(2) + '-' + stop_timetable[1] + '.json', 'w')  # TODO proper path support
                stop_json = {"legend": []}
                stop_json_id = stop_timetable[1]
                print('!important ', line_num, route_mem[1], stop_json_id)
                stop_timetable = False

        if not section_RP and AUX_PARSNG:
            # actually, scrap that
            # we want to save symbols, which come after 
            # if current_file:
            #     json.dump(stop_json, current_file, indent=4)
            #     current_file.close()
            #     current_file = None  # files after closing are still fp objects
            pass

        if (not section_TD) and AUX_PARSNG:
            if stop_json_id:
                if JSON_OUT[line_num][route_mem[1]].get('timetables', False):
                    JSON_OUT[line_num][route_mem[1]]['timetables'][stop_json_id] = stop_json
                else:
                    JSON_OUT[line_num][route_mem[1]]['timetables'] = {stop_json_id: stop_json}
                # stop_json = None
                stop_json_id = None

        if (section_TD or section_OP) and AUX_PARSNG:
            # save everything to stop timetable file (?)
            # if current_file:
                # Try getting day symbol that comes after *TD
            day_symbol = re.match(r" {21}(\w\w)  (.+)", line)  # DP / DZIEN POWSZEDNI
            if day_symbol:
                last_symbol = day_symbol[1]
                stop_json[last_symbol] = {"timetable": {}, "departures": {}}

                # TODO: if section_OP: stop_json['legend'] = all

                #current_file.write(line)

        if section_WG and AUX_PARSNG:
            times = re.match(TIMETABLE_HUMAN, line)
            if times:
                hour, minutes = times[1], times[2]
                stop_json[last_symbol]["timetable"][hour] = minutes.split()

        if section_OD and AUX_PARSNG:
            departures = re.match(TIMETABLE_DEPARTURES, line)
            if departures:
                _time, trip_id = departures[1], departures[2]
                stop_json[last_symbol]["departures"][_time] = trip_id

        if section_OP and AUX_PARSNG:
            legend = re.match(TIMETABLE_LEGEND, line)
            if legend:
                stop_json["legend"].append(legend[1] + ' ' + legend[2])

    return JSON_OUT


if __name__ == '__main__':
    with open('RA220202.TXT', 'r') as f:
        data = parse_route_info(f)
        with open(f'output.json', 'w') as t:
            json.dump(data, t, indent=4)
