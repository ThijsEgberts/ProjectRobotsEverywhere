#import the neccecary packages
    import numpy as np
    from PIL import Image

def check_image(image): ##image path as string example: 'image.png'
    
    #setting treshold for detection (red and blue values)
    treshold_red = 200
    treshold_blue = 100

    image_array = np.array(Image.open(image).convert('RGB')) #import the image as an array

    #compare pixels to threshold values
    red_mask = image_array[:,:, 0] > treshold_red
    blue_mask = image_array[:,:,2] < treshold_blue

    mask = red_mask & blue_mask #combine both masks

    coordinates = np.where(mask) #convert mask to coordinates

    #cluster the data
    clust = [np.mean(coordinates[0][:]),np.mean(coordinates[1][:])]
    
    return clust
