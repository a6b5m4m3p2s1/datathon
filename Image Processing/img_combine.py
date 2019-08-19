"""
Created on Mon Aug 18 12:56:52 2019

@author: matt

Combine all the tiles for a particular date horizontally

Note: Produces the warning 
        "FutureWarning: arrays to stack must be passed as a "sequence" type such as list or tuple. Support for 
         non-sequence iterables such as generators is deprecated as of NumPy 1.16 and will raise an error in the future"
      ToDo: Try to eliminate this.

"""
import numpy as np
from PIL import Image  
from functions_image import img_grey_to_rgb


tile_date_list = 'files.txt'
save_folder = './data/Combined/By Date/'
# The initial release contains only one tile, so lets hard-code its location here.  When you have more tiles, you can update this
TILE_X = 7680
TILE_Y = 10240
path = f"./data/sentinel-2a-tile-{TILE_X}x-{TILE_Y}y/timeseries/{TILE_X}-{TILE_Y}-"

with open(tile_date_list) as f:
    content = f.readlines()
content = [x.strip() for x in content]

for dt in range(len(content)):
    tile_date = content[dt]

    img_band = []
    for x in range(1, 13):
        img_band.append (f"B{x:02d}")
    
    img_band.insert (8, "B8A")
    img_band.append ("TCI")
    
    for x in range(len(img_band)):
    	img_band[x] = f"{path}{img_band[x]}-{tile_date}.png"
    	
    imgs = []
    for x in range(len(img_band)):
        imgs.append(img_grey_to_rgb(img_band[x]))
    
    imgs_comb = np.hstack(np.asarray(i) for i in imgs )         # Stack image data arrays
    imgs_comb = Image.fromarray(imgs_comb)                      # Convert to image
    imgs_comb.save(save_folder + tile_date + '.png' )           # Save
    