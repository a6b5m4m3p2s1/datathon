import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

"""
Created on Sun Aug 18 14:35:16 2019

@author: matt
"""

from functions_image import img_grey_to_rgb

year_date_files = 'year_dates.csv'
year_dates = [line.split(',') for line in open(year_date_files)]
year_dates = [[s.strip() for s in nested] for nested in year_dates]  # Strip special chars. Nested since 2D list

TILE_X = 7680
TILE_Y = 10240
save_folder = './data/Combined/By Year/'
path_tiles = f"./data/sentinel-2a-tile-{TILE_X}x-{TILE_Y}y/timeseries/{TILE_X}-{TILE_Y}-TCI-"
path_extra = "./extra_tiles/512x512_"

imgs_comb = []
for rw in range(1, len(year_dates)):
    row_tiles = year_dates[rw][1:]       # Drop label column
    img_date = [(path_extra if len(i) < 6 else path_tiles) + i + ".png" for i in row_tiles]
    
    imgs = []
    for x in range(len(img_date)):
        imgs.append(img_grey_to_rgb(img_date[x], quiet = True))
    
    imgs_row = np.hstack((np.asarray(i) for i in imgs))
    imgs_comb.append(Image.fromarray(imgs_row))

    plt.imshow(imgs_comb[-1])
    plt.show(imgs_comb[-1])

imgs_all = np.vstack((np.asarray(i) for i in imgs_comb))
imgs_all = Image.fromarray(imgs_all)

imgs_all.save(save_folder + 'TCI_All' + '.png' )  
plt.imshow(imgs_all)
plt.show(imgs_all)

    
