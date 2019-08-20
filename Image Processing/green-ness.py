# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 12:12:47 2019

@author: matt
"""

import matplotlib.pyplot as plt
from PIL import Image
from functions_image import draw_text_centred

ix = 20     # width of individual images
iy = 20     # height of individual images

sr = 94     # start values (top left)
sg = 38
sb = 20

er = 0     # end values (top right)
eg = 255
eb = 0

cr = er - sr    # change in values (top left to top right)
cg = eg - sg
cb = eb - sb

px = 400 #cg         # Nominal width one pixel per green gradation. 
py = 250  #100

gx = 20         # Granulartity 
gy = 20

wx = int(px / gx )
wy = int(py / gy)

print (wx, wy)
#ir = 255 - sr
ig = 255 - sg

ckr = 10
img = Image.new('RGBA', (wx * gx, wy * gy))
print (img.size)
pixels = img.load()

gn_limit = 0.32
prev_gn_row = 0
prv_clr_row = (0, 0, 0)
for x in range(gx):
    r = sr + x * cr / (gx - 1)
    g = sg + x * cg / (gx - 1)
    b = sb + x * cb / (gx - 1)
    print (x) #, r, g, b)
    prev_gn_col = int(100 * g / (r + g + b)) / 100
    for y in range(gy):
        pr = int(r + y * ((255 - r) / gy))
        pg = int(g + y * ((255 - g) / gy))
        pb = int(b + y * ((255 - b) / gy))
        greenness = int(100 * pg / (pr + pg + pb)) / 100
        gn_chg_col = True if prev_gn_col >= gn_limit and greenness < gn_limit else False

        if x == 0:
            prv_r, prv_g, prv_b = 0, 0, 0
        else:
            prv_r = sr + (x - 1) * cr / (gx - 1)
            prv_g = sg + (x - 1) * cg / (gx - 1)
            prv_b = sb + (x - 1) * cb / (gx - 1)
            
            prv_r = int(prv_r + y * ((255 - prv_r) / gy))
            prv_g = int(prv_g + y * ((255 - prv_g) / gy))
            prv_b = int(prv_b + y * ((255 - prv_b) / gy))
            
            prev_gn_row = int(100 * prv_g / (prv_r + prv_g + prv_b)) / 100
    
        gn_chg_row = True if prev_gn_row < gn_limit and greenness >= gn_limit else False
        print (greenness, prev_gn_col, gn_chg_col, prev_gn_row, gn_chg_row)
        
        for mx in range(wx):
            for my in range(wy):
                clr = (0, 0, 0) if (mx == 0 and gn_chg_row) or (my == 0 and gn_chg_col) else (pr, pg, pb)
                pixels[x * wx + mx, y * wy + my] = clr
        prev_gn_col = greenness

lbl = str(gn_limit)
img = draw_text_centred(img, lbl, font_size = 30, text_clr = (0,0,0), font_file = 'Calibri.ttf', boundary_x = (0.85, 0.95), boundary_y = (0.05, 0.25))
        
plt.imshow(img)
plt.show(img) 
img.save('greens/green-ness_' + str(gn_limit) + '.png')

