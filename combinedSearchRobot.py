#! /usr/bin/python3
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
from scipy import ndimage
import argparse
from threading import Thread, Event

#For this program we use all carthesian coordinates for simplicities sake
#For a real world program the implementation of the functions would have to be different to accomidate drone control software and gps locations instead of carthesian coordinates
#I have also left out these conversian functions since they don't add to this program

parser = argparse.ArgumentParser(description='Thermal Camera Program')
parser.add_argument('--noInterpolation', dest='noInterpolation', action='store_const', default='true',
                    const='noInterpolation', help='Interpolate the image when detecting heat (default: true)')
args = parser.parse_args()
noInterpolation = args.noInterpolation

if(noInterpolation == 'true'):
    print('Interpolation mode: true')
    mlx_interp_val = 3 # interpolate # on each dimension
else:
    print('Interpolation mode: false')
    mlx_interp_val = 1 # interpolate # on each dimension


threshhold = 33 #in degrees
shared_var = Event()


i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # set refresh rate
mlx_shape = (24,32) # mlx90640 shape

mlx_interp_shape = (mlx_shape[0]*mlx_interp_val,
                    mlx_shape[1]*mlx_interp_val) # new shape


fig = plt.figure(figsize=(12,9)) # start figure
ax = fig.add_subplot(111) # add subplot
fig.subplots_adjust(0.05,0.05,0.95,0.95) # get rid of unnecessary padding
therm1 = ax.imshow(np.zeros(mlx_interp_shape),interpolation='none',
                   cmap=plt.cm.bwr,vmin=0,vmax=45) # preemptive image

fig.canvas.draw() # draw figure to copy background
ax_background = fig.canvas.copy_from_bbox(ax.bbox) # copy background
fig.show() # show the figure before blitting

frame = np.zeros(mlx_shape[0]*mlx_shape[1]) # 768 pts

def detect_heat(shared_var):
    #fig.canvas.restore_region(ax_background) # restore background
    
    mlx.getFrame(frame) # read mlx90640
    
    data_array = np.fliplr(np.reshape(frame,mlx_shape)) # reshape, flip data
    
    #do the detection before the interpolation
    mask = data_array[:,:] > threshhold #check if there are temprature readings of over 37

    
    coordinates = np.asarray(mask).nonzero() #get the coordinates where there is heat
    
    ##data_array = ndimage.zoom(data_array,mlx_interp_val) # interpolate
    #therm1.set_array(data_array) # set data
    ##therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
    #therm1.set_clim(vmin=20,vmax=40) # set bounds
    
    heatInImage = np.any(coordinates)
    #print("Is there a person in the image: " + str(heatInImage))
    if heatInImage:
        shared_var.set() #signal the other thread that heat has been detected
        print('Heat detected')
    #    center = np.mean(coordinates)
    #    print(center)
    #    squared_dist = (center[0] - 0)**2 + (center[1] - 0)**2
    #    print(squared_dist)
    print_image(data_array)

    #plt.pause(0.001)
    #ax.draw_artist(therm1) # draw new thermal image
    ##fig.canvas.blit(ax.bbox) # draw background
    #fig.canvas.flush_events() # show the new image
    #fig.show()
    return
    
def print_image(image):
    fig.canvas.restore_region(ax_background) # restore background
    
    
    image = ndimage.zoom(image,mlx_interp_val) # interpolate
    therm1.set_array(image) # set data
    #therm1.set_clim(vmin=np.min(image),vmax=np.max(image)) # set bounds
    therm1.set_clim(vmin=20,vmax=40) # set bounds
    
  
    
    plt.pause(0.001)
    ax.draw_artist(therm1) # draw new thermal image
    #fig.canvas.blit(ax.bbox) # draw background
    fig.canvas.flush_events() # show the new image
    fig.show()
    
    
    return

def image_detection(shared_var):
	t_array = []
	while True:
		t1 = time.monotonic() # for determining frame rate
		try:
			detect_heat(shared_var) # update plot
		except Exception as e:
			#print("The exception is:")
			print(e)
			continue
		# approximating frame rate
		#t_array.append(time.monotonic()-t1)
		#if len(t_array)>10:
	#		t_array = t_array[1:] # recent times for frame rate approx
	#	print('Frame Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))


#function to simulate the drone control software that blocks the main loop until the drone has arrived
def moveTo(loc):
	#placeholder, put the drone control code here for a real example
	print("Move the drone to (" + str(loc[0]) + ", " + str(loc[1]) + ")")
	inp = input("Give terminal input when the drone has arrived")


#this function calculates the next location based on a cone shaped search pattern
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

#this function calculates the next location in carthesiean coordinates based on an adapted square search pattern
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

def keepTargetCentered():
	print("try to keep the target centered")
	return


def pathFinding(shared_var):
	current_loc = [0,0]#init location
	next_loc = nextLoc(current_loc)

	while not shared_var.is_set():	
		next_loc = nextLoc(current_loc)
		#next_loc = cone(current_loc, 1)
		moveTo(next_loc)
		current_loc = next_loc
	print('stopped searching')
	print('The location of the victim is ' + str(current_loc))
	#while True:
#		keepTargetCentered()


#synchronasation
if __name__ == '__main__':
	pathFindingThread = Thread(target=pathFinding, args=(shared_var, ))
	#detectionThread = Thread(target=image_detection)
	
	#detectionThread.start()
	
	pathFindingThread.start()
	
	data_array = np.fliplr(np.reshape(frame,mlx_shape))
	print_image(data_array)
	
	image_detection(shared_var)
	#pathFindingThread.join()
	detectionThread.join()
