import os
from PIL import Image
import numpy as np

img = Image.open('toudai.jpg')

width, height = img.size
img2 = Image.new('RGB', (width, height))
print(width, heightf)

img_pixels = []
for y in range(height):
    for x in range(width):
        img_pixels.append(img.getpixel((x,y)))
img_pixels = np.array(img_pixels)
print(img_pixels.shape)
