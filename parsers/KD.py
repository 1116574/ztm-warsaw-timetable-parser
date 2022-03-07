def KD(f):
    import re
    result = {}

    for line in f:
        if line.startswith('#KD'):
            return result

        match = re.match(r' +([^ ]+)   (\w\w)\n', line)
        if match:
            result[match[1]] = match[2]
