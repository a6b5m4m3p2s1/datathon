# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 18:28:09 2019

@author: matt
"""

import numpy as np
#import matplotlib.pyplot as plt
from PIL import Image

# The initial release contains only one tile, so lets hard-code its location here.  When you have more tiles, you can update this
TILE_X = 7680
TILE_Y = 10240
TILE_LOCN   = f'{TILE_X}-{TILE_Y}'
TILE_LOCNxy = f'{TILE_X}x-{TILE_Y}y'

# Tile width / height in pixels
TILE_WIDTH_PX = 512
TILE_HEIGHT_PX = 512
TILE_SIZE_PX = (TILE_WIDTH_PX, TILE_HEIGHT_PX)

TILE_DATE_LIST = 'files.txt'
SAVE_FOLDER =  '../data/processed/Combined/By Channel/'
PATH_TILES  = f'../data/unprocessed/sentinel-2a-tile-{TILE_LOCNxy}/timeseries/{TILE_LOCN}-TCI-'
PATH_MASK   =  '../data/processed/mask/'

img_mask = Image.open(f'{PATH_MASK}{TILE_LOCNxy}-mask_fixed.png')

with open(TILE_DATE_LIST) as f:
    dt_list = f.readlines()
f.close()

dt_list = [x.strip() for x in dt_list]
tile_list = [f'{PATH_TILES}{x}.png' for x in dt_list]

"""
# List of channels for extraction from main image
# Allows looping for channels rather than hard-coding
# Each row represents a channel to extract
# Each of the 3 lists in the row represents the makeup of the output channel
# The innermost list represents how the output channel is made up, so row 4 = red channel 
# output to RGB channels, so a greyscale image of the red channel.
# Based on an idea from https://stackoverflow.com/questions/51325224/python-pil-image-split-to-rgb
clr_ch
"""
clr_ch = [[[1, 0, 0], [0, 0, 0], [0, 0, 0]],                 # Red channel                \ 
          [[0, 0, 0], [0, 1, 0], [0, 0, 0]],                 # Green channel              \
          [[0, 0, 0], [0, 0, 0], [1, 0, 0]],                 # Blue channel               \
          [[1, 0, 0], [1, 0, 0], [1, 0, 0]],                 # Red channel as greyscale   \
          [[0, 1, 0], [0, 1, 0], [0, 1, 0]],                 # Green channel as greyscale \
          [[0, 0, 1], [0, 0, 1], [0, 0, 1]]]                 # Blue channel as greyscale  


# Horizontally stitch all tiles for each date
imgs_all = []
for dt in range(len(dt_list)):
    tile_date = dt_list[dt]
    print(dt_list[dt], tile_list[dt])
    
    img_TCI = Image.open(tile_list[dt])
    img_masked = Image.alpha_composite(img_TCI.convert('RGBA'), img_mask).convert('RGB')

    img_data = img_masked.getdata()
    m = [(d[0], d[1], d[2]) for d in img_data]

    imgs = []
    imgs.append(img_TCI)
    imgs.append(img_masked)
    
    for ch in range(len(clr_ch)):
        img_ch = Image.new('RGB', TILE_SIZE_PX, color = (0, 0, 0))
        # Multiply and sum each channel from masked TCI data by matrix to get desired channel as colour or greyscale
        # There should be a more efficient way to do this using np.multiply, but I haven't spent time on it yet.
        cc = clr_ch[ch]
        img_ch.putdata([(d[0] * cc[0][0] + d[1] * cc[0][1] + d[2] * cc[0][2], \
                         d[0] * cc[1][0] + d[1] * cc[1][1] + d[2] * cc[1][2], \
                         d[0] * cc[2][0] + d[1] * cc[2][1] + d[2] * cc[2][2]) for d in img_data])
        imgs.append(img_ch)

    imgs_comb = np.hstack(np.asarray(i) for i in imgs)          # Stack image data arrays
    imgs_comb = Image.fromarray(imgs_comb)                      # Convert to image
    imgs_comb.save(f'{SAVE_FOLDER}{dt_list[dt]}.png')
    imgs_all.append(imgs_comb)

imgs_all_comb = np.vstack(np.asarray(i) for i in imgs_all)          # Stack image data arrays
imgs_all_comb = Image.fromarray(imgs_all_comb)                      # Convert to image
imgs_all_comb.save(f'{SAVE_FOLDER}All.png')
