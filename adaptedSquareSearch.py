#this function calculates the next location in carthesiean coordinates based on an adapted square search pattern
#only works with integer coordinates
def nextLoc(location):

    new_loc = []
    x = location[0]
    y = location[1]
    
    if y < 0 and -y > abs(x):
        #zone 1
        if y % 2 == 0:
            new_loc = [x + 1, y]
        else:
            new_loc = [x - 1, y]
                
    elif y > 0 and y > abs(2*x):
        #zone 2
        temp_new_loc = []
        
        if y % 4 == 0:
            temp_new_loc = [x - 1, y]
        elif y % 4 ==1:
            temp_new_loc = [x - 1, y]
        elif y % 4 ==2:
            temp_new_loc = [x + 1, y]
        else:
            temp_new_loc = [x + 1, y]
            
        print(temp_new_loc)
        
        #check if outside zone 2, if so move up
        if temp_new_loc[1] < abs(2*temp_new_loc[0]):
            new_loc = [x, y+1]
        else:
            new_loc = temp_new_loc
        
    elif x > 0 and -x < y < 2*x:
        #zone 3
        if x % 2 == 0:
            new_loc = [x, y + 1]
        else:
            new_loc = [x, y - 1]
                
    elif x < 0 and x < y < -2*x:
        #zone 4
        if x % 2 == 0:
            new_loc = [x, y - 1]
        else:
            new_loc = [x, y + 1]
                
    elif y < 0 and x == -y:
        #coll 1 3
        if x % 2 == 0:
            new_loc = [x, y + 1]
        else:
            new_loc = [x - 1, y]
        
    elif y < 0 and x == y:
        #coll 1 4
        if x % 2 == 0:
            new_loc = [x + 1, y]
        else:
            new_loc = [x, y + 1]
        
    elif y > 0 and y == 2*x:
        #coll 2 3
        if x % 2 == 0:
            new_loc = [x, y + 1]
        else:
            new_loc = [x, y - 1]
    
    elif y > 0 and y == -2*x:
        #coll 2 4
        if x % 2 == 0:
            new_loc = [x, y - 1]
        else:
            new_loc = [x, y + 1]
    
    else:
        new_loc = [x, y + 1]
        
    return new_loc
