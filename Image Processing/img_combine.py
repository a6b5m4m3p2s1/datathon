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
import matplotlib.pyplot as plt
from PIL import Image  
from functions_image import img_grey_to_rgb, draw_text_centred

# The initial release contains only one tile, so lets hard-code its location here.  When you have more tiles, you can update this
TILE_X = 7680
TILE_Y = 10240
# Tile width / height in pixels
TILE_WIDTH_PX = 512
TILE_HEIGHT_PX = 512

TILE_DATE_LIST = 'files.txt'
SAVE_FOLDER = '../data/processed/Combined/By Date/'
PATH_TILES = f"../data/unprocessed/sentinel-2a-tile-{TILE_X}x-{TILE_Y}y/timeseries/{TILE_X}-{TILE_Y}-"

with open(TILE_DATE_LIST) as f:
    content = f.readlines()
content = [x.strip() for x in content]

# Horizontally stitch all tiles for each date
for dt in range(len(content)):
    tile_date = content[dt]

    # Create list of tile names B01, B02, B03, B04, B05, B06, B07, B08, B8A, B09, B10, B11, B12, TCI
    img_band = []
    for x in range(1, 13):
        img_band.append (f"B{x:02d}")
    img_band.insert (8, "B8A")
    img_band.append ("TCI")
    
    # Add file path
    for x in range(len(img_band)):
    	img_band[x] = f"{PATH_TILES}{img_band[x]}-{tile_date}.png"
    
    # List of tiles images	
    imgs = []
    for x in range(len(img_band)):
        imgs.append(img_grey_to_rgb(img_band[x]))
    
    imgs_comb = np.hstack(np.asarray(i) for i in imgs)          # Stack image data arrays
    imgs_comb = Image.fromarray(imgs_comb)                      # Convert to image
    imgs_comb.save(SAVE_FOLDER + tile_date + '.png' )           # Save
    

# Vertically stitch all images created above
img_date = [SAVE_FOLDER + x + ".png" for x in content]          # Add all tiles to a list
imgs     = [Image.open(i) for i in img_date]                    # Open all images    
    
imgs_comb = np.vstack(np.asarray(i) for i in imgs)              # Stack image data arrays
imgs_comb = Image.fromarray(imgs_comb)                          # Convert to image
imgs_comb.save(SAVE_FOLDER + 'all.png')                         # Save



# Stitch TCI (colour) tiles by period (cols) and year (rows) so that tiles from the same time of the year align vertically
# year_dates.csv gives layout, including missing tiles and border label tiles

YEAR_DATE_FILE = 'year_dates.csv'
year_dates = [line.split(',') for line in open(YEAR_DATE_FILE)]
year_dates = [[s.strip() for s in nested] for nested in year_dates]  # Strip special chars. Nested since 2D list

SAVE_FOLDER = '../data/processed/Combined/By Year/'
PATH_TILES = f"{PATH_TILES}TCI-"
PATH_EXTRA = f"./extra_tiles/{TILE_WIDTH_PX}x{TILE_HEIGHT_PX}_"

imgs_comb = []
for rw in range(1, len(year_dates)):
    row_tiles = year_dates[rw][1:]                                  # Drop label column
    img_date = [(PATH_EXTRA if len(i) < 6 else PATH_TILES) + i + ".png" for i in row_tiles]
    
    imgs = []
    for x in range(len(img_date)):
        imgs.append(img_grey_to_rgb(img_date[x], quiet = True))
    
    imgs_row = np.hstack((np.asarray(i) for i in imgs))
    imgs_comb.append(Image.fromarray(imgs_row))

    plt.imshow(imgs_comb[-1])
    plt.show(imgs_comb[-1])

img_all = np.vstack((np.asarray(i) for i in imgs_comb))
img_all = Image.fromarray(img_all)

img_all.save(SAVE_FOLDER + 'TCI_All' + '.png' )  


# Add border tiles and row & column titles
FONT_FILE = 'Calibri.ttf'
FONT_SIZE = 100
TEXT_FILL = (255, 255, 0)               # Yellow

col_titles = year_dates[0][1:]          # Drop label column
text_y = (0, TILE_HEIGHT_PX)
for x in range(len(col_titles)):
    msg = col_titles[x]
    text_x = tuple(np.add((0, TILE_HEIGHT_PX), (TILE_WIDTH_PX * x, TILE_HEIGHT_PX * x)))
    img_all = draw_text_centred(img_all, msg, FONT_SIZE, TEXT_FILL, FONT_FILE, text_x, text_y)

row_titles = [row[0] for row in year_dates][1:]
print(row_titles)
tiles_x = len(col_titles) 
text_x = (0, TILE_HEIGHT_PX)
text_x2 = (TILE_WIDTH_PX * (tiles_x - 1), TILE_HEIGHT_PX * tiles_x)
for x in range(len(row_titles)):
    msg = row_titles[x]
    text_y  = tuple(np.add((0, TILE_HEIGHT_PX), (TILE_WIDTH_PX * x, TILE_HEIGHT_PX * x)))
    img_all = draw_text_centred(img_all, msg, FONT_SIZE, TEXT_FILL, FONT_FILE, text_x, text_y)
    img_all = draw_text_centred(img_all, msg, FONT_SIZE, TEXT_FILL, FONT_FILE, text_x2, text_y)

plt.imshow(img_all)
plt.show(img_all)   