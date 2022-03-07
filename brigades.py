# Creates an index to be used in realtime (RT) applications
# Basically, RT data is provided in a weird format and to map individual busses to their timetables you need to hit API endpoint with a bunch of data.
# This does that and then saves the result so it may be used through the day

# Some of this code is a 2-3 years old at this point so it may differ from rest of the codebase

import json
from collections import defaultdict
import argparse

import requests

# debug
from rich import print


def _api_translator(api_response):
    """ Returns prettier json """
    if (type(api_response) is str) or (type(api_response['result']) is str):
        return False

    pretty = []

    api_response = api_response['result']

    for item in api_response:
        item = item['values']

        item = {
            'sign_2': item[0]['value'],
            'sign_1': item[1]['value'],
            'brigade': item[2]['value'],
            'heading': item[3]['value'],
            'route': item[4]['value'],
            'time': item[5]['value'],
        }

        pretty.append(item)

    return pretty


# request_queue = {
#     'line-num': {
#         'stopid': [
#             ('trip_id', 'time'),
#             ('trip_id', 'time'),
#             ('trip_id', 'time')
#         ]
#     }
# }


def create_queue(stop_times):
    request_queue = defaultdict(dict)

    for line in stop_times:
        for trip_id in stop_times[line]:
            # Now we look for a stop that we can make request with.
            # Specifically, we try to avoid "B" flags since that means trip is non-standard, and therfore probability of getting multiple trip ids is low.
            for stop in stop_times[line][trip_id]:
                stop_id, time, flag = stop
                if flag == 'B':
                    continue
                else:
                    # print(type(request_queue[line].get(stop_id, None)))
                    if type(request_queue[line].get(stop_id, None)) is list:
                        request_queue[line][stop_id].append((trip_id, time))
                        break
                    else:
                        request_queue[line][stop_id] = [(trip_id, time)]
                        break

    return request_queue


def match(request_queue, APIKEY):
    output = defaultdict(dict)
    for line in request_queue:
        if line == '11':
            break
        for stop in request_queue[line]:
            # print(request_queue[line][stop])
            stop_nr = stop[4:]
            stop_id = stop[:4]

            print(f'Making request for stop {stop_id} {stop_nr} and line {line}')

            details_url = f'https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&apikey={APIKEY}'
            response = requests.get(details_url, params={'busstopId': stop_id, 'busstopNr': stop_nr, 'line': line})
            response.raise_for_status()

            response = _api_translator(response.json())
            if not response:
                print('Api error, skipping')
                continue

            # print(response)
            # return response

            for departure in response:
                for entry in request_queue[line][stop]:
                    # print('bbb', line, entry[1], departure['time'], departure['brigade'], departure['heading'])
                    trip_time = entry[1].replace('.', ':')  # 12:40
                    # print(trip_time)
                    trip_time += ':00'
                    if len(trip_time) != 8:
                            trip_time = '0' + trip_time

                    # TODO: 32h time format testing
                    if departure['time'] == trip_time:  # It matches!
                        # print('aaaa', line, entry[0], departure['brigade'], departure['heading'])
                        output[line][entry[0]] = {
                            'brigade': departure['brigade'],
                            'heading': departure['heading']  # nice bonus, especially for exceptional routes (to depot etc), I guess?
                        }

    return output


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', '--save', help='Save request_queue (default: False)', default=False, action='store_true')
    argparser.add_argument('-r', '--requests', help='Hit API from saved request_queue file (default: False)', default=False, action='store_true')
    argparser.add_argument('-o', '--offline', help='Dont make any web requests, just save the file (default: False)', default=False, action='store_true')
    args = argparser.parse_args()
    print(args)

    with open('output/stop_times.json', 'r') as f:
        stop_times = json.load(f)

    if not args.requests:
        request_queue = create_queue(stop_times)
    else:
        with open('output/request_queue.json', 'r') as f:
            request_queue = json.load(f)        

    if args.save:
        with open(f'output/request_queue.json', 'w') as t:
            json.dump(request_queue, t, indent=4)

    try:
        with open('apikey.txt', 'r') as f:
            APIKEY = f.read()
    except FileNotFoundError:
        print('You havent provided apikey.txt file!')
        quit()

    if args.requests:
        with open('output/request_queue.json', 'r') as f:
            request_queue = json.load(f)

    if not args.offline:
        brigades = match(request_queue, APIKEY)

        with open(f'output/brigades.json', 'w') as t:
            json.dump(brigades, t, indent=4)
