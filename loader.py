import re

def load_labels(filename):
    """
    Load labels from a given file into a dictionary object
    """
    with open(filename) as f:
        contents = f.read()
    
    result = dict()
    lines = contents.splitlines()
    
    for line in lines:
        if line.startswith('#'):
            continue
        values = re.split('[ ]+', line)
        if len(values) == 1:
            # single value represents
            # the number of coordinates
            continue
        
        if len(values) == 5:
            result[values[0]] = values[1:]
    
    return result