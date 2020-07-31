import numpy as np
from PIL import Image
import utils

scale = 0.25
pil_img = Image.open('castle.jpg')  # read in image
pil_img.thumbnail((pil_img.size[0] * scale, pil_img.size[1] * scale), Image.ANTIALIAS)

color_img = np.array(pil_img)  # cast to numpy array (h * w * c)

carved = [pil_img]

print("Before, ", color_img.shape)
Image.fromarray(color_img).save('before.jpg')

for i in range(100):
    print("Seam carving {} ...".format(i))
    color_img = utils.seam_carve(color_img)
    pad = np.ones((color_img.shape[0], i + 1, 3)) * 255
    save_img = np.concatenate((color_img, pad.astype(np.uint8)), axis=1)
    carved.append(Image.fromarray(save_img))

print("After, ", color_img.shape)
Image.fromarray(color_img).save('after.jpg')

carved[0].save('demo.gif', format='GIF', append_images=carved[1:], save_all=True, duration=100, loop=0)




