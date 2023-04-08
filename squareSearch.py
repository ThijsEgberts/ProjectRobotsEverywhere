#Returns the next location based on the current location according to a square search pattern
#Only works with integer coordinates
def nextloc(location):
    new_loc = []
    x = location[0]
    y = location[1]

    if abs(x) > abs(y):
        if x > 0:
            new_loc = [x, y - 1]
        else:
            new_loc = [x, y + 1]
    else:
        if abs(x) < abs(y):
            if y > 0:
                new_loc = [x + 1, y]
            else:
                new_loc = [x - 1, y]
        else:# abs(x) = abs(y)
            if x > 0:
                if y > 0:
                    new_loc = [x + 1, y]
                else:
                    new_loc = [x - 1, y]
            else:
                if x < 0:
                    if y > 0:
                        new_loc = [x + 1, y]
                    else:
                        new_loc = [x, y + 1]
                else:
                    new_loc = [x + 1, y]
                    
    return new_loc 
