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

def load_vtk(filename):
    """
    Load vtk image into a dictionary object
    """
    with open(filename) as f:
        contents = f.read()
    
    result = dict()
    lines = contents.splitlines()
    mode = 'header'
    point_idx = 0
    num_points = None
    
    for line in lines:
        if line.startswith('#'):
            continue
        values = re.split('[ ]+', line)
        
        if mode == 'points':
            result[point_idx] = (values[0], values[1], values[2])
            
            point_idx += 1
            if point_idx == num_points:
                break
        
        if len(values) == 5:
            result[values[0]] = values[1:]
        
        if values[0] == 'POINTS':
            mode = 'points'
            num_points = int(values[1])
    
    return result