import json
import datetime
import argparse
import os

from parsers import LL
from parsers import ZP
from parsers import KD

# debug
from rich import print


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Process data from Warsaw public transit authority to json format[s]')
    argparser.add_argument('-s', '--stops', help='Parse stops (default: True)', default=True, action='store_false')
    argparser.add_argument('-r', '--routes', help='Parse routes (default: True)', default=True, action='store_false')
    argparser.add_argument('-t', '--timetables', help='Parse timetables (default: True)', default=True, action='store_false')
    argparser.add_argument('-sm', '--symbols', help='Parse symbols (default: True)', default=True, action='store_false')
    argparser.add_argument('-st', '--stop_times', help='Parse stop_times (used in RT) (default: True)', default=True, action='store_false')
    argparser.add_argument('-c', '--calendar', help='Parse calendar (used in RT) (default: True)', default=True, action='store_false')
    argparser.add_argument('-f', '--file', help='name of input file (default: get latest from web)', default=False)
    # TODO: add output path
    args = argparser.parse_args()
    print(args)

    PARSE_STOPS = args.stops
    FILE = args.file


    if not FILE:
        today = datetime.datetime.now()
        today = today.strftime('%y%m%d')
        filename = f'RA{today}.TXT'
        if filename in os.listdir():
            FILE = filename
        else:
            print('Attmpting to download files')
            from ftp_downloader import get_file
            get_file()
    else:
        filename = args.file

    with open(filename, 'r') as f:
        for line in f:
            cache = []  # ?

            # File structure looks like this:
            # *TOPLEVELTAG
            #    Key
            #       *2nd TAG
            #           Key
            #               *3rd TAG
            #                    A
            #                    B
            #                    C
            #               #3rd TAG
            #           Other Key
            #               ...
            #       #2nd TAG
            #    Key
            #    ...
            #
            # Top level tags dont have keys, hence they are parsed here in a different matter.
            # Otherwise once tag is detected file is handed off to a parser which regexes for keys in this tag, and then calls another parser which looks for keys inside that tag etc.
            # They all return some data on each step


            # What type of timetable each line uses today
            if line.find('*KD') > -1:
                calendar = KD.KD(f)

            # Stop descriptions
            if line.find('*ZP') > -1 and PARSE_STOPS:
                # Handoff to parser
                stop_groups = ZP.ZP(f)
                pass

            # save
            # Route descriptions and timetables
            # LL ─┬ TR ─┬ RP ─┬ TD ─┬ WG
            #     └ WK  └ LW  └ OP  └ OD
            if line.find('*LL') > -1:
                # Handoff to parser
                routes, timetables, symbols, stop_times = LL.LL(f, parse_routes=args.routes, parse_timetables=args.timetables, parse_symbols=args.symbols, parse_stop_times=args.stop_times)
                # print(result)

    if args.calendar:
        with open(f'output/calendar.json', 'w') as t:
            json.dump(calendar, t, indent=4)

    if args.routes:
        with open(f'output/routes.json', 'w') as t:
            json.dump(routes, t, indent=4)
    
    if args.timetables:
        with open(f'output/timetables.json', 'w') as t:
            json.dump(timetables, t, indent=4)

    if args.symbols:
        with open(f'output/symbols.json', 'w') as t:
            json.dump(symbols, t, indent=4)
        
    if args.stop_times:
        with open(f'output/stop_times.json', 'w') as t:
            json.dump(stop_times, t, indent=4)

    if PARSE_STOPS:
        with open(f'output/stop_groups.json', 'w') as t:
            json.dump(stop_groups, t, indent=4)

    