# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 12:56:52 2019

@author: matt

Collection of functions for image manipulation
"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

"""
To stitch together the satellite images provided, the simple method is to use numpy.hstack and vstack, which join the 
3D arrays that make up the images. For the datathon, the TCI images are colour in 3 channels (RGB) at 8 bits per channel
(24 bits per pixel) and the rest are greyscale at 16 bit per pixel (stored as 32 bit signed integers). This difference 
in the third dimensions of the array breaks hstack is grey images are joined to colour.

Pillow contains a Convert method to convert between image modes (see pillow.readthedocs.io/en/4.1.x/handbook/concepts.html#modes)
However, when this is applied to the greyscale satellite images, it returns the wrong thing - a mostly grey image comes 
back as almost all white.  

For this reason, I wrote this to do a crude conversion from grey to RGB

source_file: string representing path and file of image
save_as:     string representing path and file to save converted image (optional)
display:     boolean if True will display converted image in IPython console
quiet:       no msg if wrong file type passed
"""
def img_grey_to_rgb(source_file, save_as = '', display = False, quiet = False):
    img_source = Image.open(source_file)
    if img_source.mode != "I":
        if not quiet:
            print(f"Processing: {source_file}")
            print("Source image is not 'I' (32-bit signed integer pixels). Returned image is same as source.")
        ret = img_source
    else:
        size = img_source.size
        pix = img_source.load()
        
        img = Image.new('RGB', size)
        pixels = img.load()                                 # create the pixel map

        for i in range(img.size[0]):                        # for every col:
            for j in range(img.size[1]):                    # For every row
                grey = pix[i, j] * (2 ** 8) / (2 ** 16)     # Convert from 16 bit grey to 8 bit (should be 16 bit positive value)
                grey = int(grey + 0.5)                      # Convert to integer (should be between 0 and 255)
                pixels[i, j] = (grey, grey, grey)           # set the colour 
        
        ret = img

    if save_as != '':
        ret.save(save_as)
    if display:
        plt.imshow(ret)
        plt.show(ret)
          
    return ret

"""
Centering text added to an image is a bit fiddly, so I wrote this.

ToDo: Doco for variables
"""

def draw_text_centred(im, msg, font_size, text_clr, font_file = '', boundary_x = (0, 0), boundary_y = (0, 0)):
    im = im.copy()                                                  # Otherwise mutates object passed (check this, may have been due to earlier error in code)
    draw = ImageDraw.Draw(im)
    if (boundary_x == (0, 0)) and (boundary_y == (0, 0)):
        text_bdry = im.size
        text_o = (0, 0)
    else:
        if boundary_x == (0, 0): boundary_x = (0, im.size[0])
        if boundary_y == (0, 0): boundary_y = (0, im.size[1])
        text_bdry = (boundary_x[1] - boundary_x[0], boundary_y[1] - boundary_y[0])
        text_o = (boundary_x[0], boundary_y[0])

    fnt = ImageFont.truetype(font_file, font_size) if font_file != '' else ImageFont.load_default()
    txt_drawn = draw.textsize(msg, font = fnt)
    txt_origin = tuple(np.subtract(text_bdry, txt_drawn) / 2)
    txt_origin = tuple(np.add(txt_origin, text_o))

    draw.text(txt_origin, msg, font = fnt, fill = text_clr)
    return im
























#### Finding font folder (ToDO) #########

#import matplotlib.font_manager as fontman
#import os
##print(fontman.findSystemFonts())
#
#def find_font_file(query):
#    matches = list(filter(lambda path: query in os.path.basename(path), fontman.findfont()))
#    return matches
#
#f = find_font_file('arialbi')
#print(f)