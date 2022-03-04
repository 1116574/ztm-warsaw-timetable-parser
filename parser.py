import json
from parsers import LL
from parsers import ZP
from rich import print


PARSE_LINES = True
PARSE_STOPS = False

if __name__ == '__main__':
    with open('RA220202.TXT', 'r') as f:
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



            # Stop descriptions
            if line.find('*ZP') > -1 and PARSE_STOPS:
                # Handoff to parser
                stop_groups = ZP.ZP(f)
                pass

            # save
            # Route descriptions and timetables
            if line.find('*LL') > -1 and PARSE_LINES:
                # Handoff to parser
                routes, timetables, symbols = LL.LL(f)
                # print(result)

    if PARSE_LINES:
        with open(f'output/routes.json', 'w') as t:
            json.dump(routes, t, indent=4)
        
        with open(f'output/timetables.json', 'w') as t:
            json.dump(timetables, t, indent=4)

        with open(f'output/symbols.json', 'w') as t:
            json.dump(symbols, t, indent=4)

    if PARSE_STOPS:
        with open(f'output/stop_groups.json', 'w') as t:
            json.dump(stop_groups, t, indent=4)

    