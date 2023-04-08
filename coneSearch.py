#this function calculates the next location based on a cone shaped search pattern
#only works with integer coordinates
def cone(location, streamspeed):
    
    new_loc = []
    x = location[0]
    y = location[1]
    
    if y % 2 == 0:
        new_loc = [x - 1, y]
    else:
        new_loc = [x + 1, y]
        
    if abs(streamspeed*new_loc[0]) > abs(new_loc[1]):
        new_loc = [x, y + 1]
    
        
    return new_loc
