# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:53:06 2019

@author: matt
"""

import numpy as np
from PIL import Image  

tile_date_list = 'files.txt'
save_folder = './data/Combined/By Date/'
path = save_folder

with open(tile_date_list) as f:
    content = f.readlines()
content = [x.strip() for x in content]
print(content)

img_date = [save_folder + x + ".png" for x in content]
imgs    = [Image.open(i) for i in img_date ]
    
# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

# save 
imgs_comb = Image.fromarray(imgs_comb)
imgs_comb.save(save_folder + 'all.png' )    