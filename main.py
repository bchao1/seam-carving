import numpy as np
from PIL import Image

img = np.asarray(Image.open('castle.jpg'))
print(img.shape)
