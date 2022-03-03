import json
from parsers import LL
from rich import print


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
            if line.find('*ZP') > -1:
                # Handoff to parser
                # result = ZP(f)
                pass

            # save
            # Route descriptions and timetables
            if line.find('*LL') > -1:
                # Handoff to parser
                result = LL.LL(f)
                print(result)

    with open(f'output/output.json', 'w') as t:
        json.dump(result, t, indent=4)

    