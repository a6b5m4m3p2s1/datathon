# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:53:06 2019

@author: matt
"""

import numpy as np
from PIL import Image  

tile_date_list = 'files.txt'
save_folder = '../data/processed/Combined/By Date/'
path = save_folder

with open(tile_date_list) as f:
    content = f.readlines()
content = [x.strip() for x in content]

img_date = [save_folder + x + ".png" for x in content]
imgs    = [Image.open(i) for i in img_date ]
    
imgs_comb = np.vstack(np.asarray(i) for i in imgs)

# save 
imgs_comb = Image.fromarray(imgs_comb)
imgs_comb.save(save_folder + 'all.png' )    