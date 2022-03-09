import re

def PR(f):
    # isnt he beautiful!
    REGEX = r" {9}(\d{6}) {2,3}\d{1,2} +Ul.\/Pl.: ([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+).+Kier.: ([0-9A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ\. \"\-\+\(\)\/]+).+Y= (\d\d\.\d+) +X= (\d\d\.\d+) +Pu=(\d)"
    # TODO: Get rid off regex and use rigid column indexes (form chars 12 to 32 its an X, from 33 to 36 its an Y etc.)
    output = {}
    # output = defaultdict(list)
    for line in f:
        if line.find('#PR') > -1:
            return output
        
        match = re.search(REGEX, line)
        if match:
            # key found, pass contents
            print(f'  PR: {match[1]}')
            # something = PR(f)
            output[match[1][4:]] = {
                "id": match[1],
                "location": match[2],
                "direction": match[3],
                "Y": match[4],
                "X": match[5],
                "accessibility": match[6]
            }
