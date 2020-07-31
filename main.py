import os
import numpy as np
from PIL import Image
import utils

exp = 'examples/tree'
imfile = 'tree.jpg'
vertical = True

# Downscale image (just for faster demo)
scale = 0.5
pil_img = Image.open(os.path.join(exp, imfile))  # read in image
pil_img.thumbnail((pil_img.size[0] * scale, pil_img.size[1] * scale), Image.ANTIALIAS)

# Cast to numpy
color_img = np.array(pil_img)  # cast to numpy array (h * w * c)

if vertical:
    color_img = np.transpose(color_img, (1, 0, 2))

carved = [pil_img]

print("Before, ", color_img.shape)

save_img = color_img
if vertical:
    save_img = np.transpose(color_img, (1, 0, 2))
Image.fromarray(save_img).save(os.path.join(exp, 'before.jpg'))

for i in range(100):
    print("Seam carving {} ...".format(i))
    color_img = utils.seam_carve(color_img)
    pad = np.ones((color_img.shape[0], i + 1, 3)) * 255
    save_img = np.concatenate((color_img, pad.astype(np.uint8)), axis=1)
    
    if vertical:
        save_img = np.transpose(save_img, (1, 0, 2))

    carved.append(Image.fromarray(save_img))

print("After, ", color_img.shape)

save_img = color_img
if vertical:
    save_img = np.transpose(color_img, (1, 0, 2))
Image.fromarray(save_img).save(os.path.join(exp, 'after.jpg'))

carved[0].save(os.path.join(exp, 'demo.gif'), 
    format='GIF', append_images=carved[1:], save_all=True, duration=100, loop=0)




