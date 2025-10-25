import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys

image_path = sys.argv[1]
img = Image.open(image_path)

img_rgb = img.convert("RGB")

img_array = np.array(img_rgb)

threshold = 30

black_mask = np.all(img_array < threshold, axis=-1)

# converts black -> white and colorful -> black
output_array = np.zeros_like(img_array)
output_array[black_mask] = [255, 255, 255]
output_array[~black_mask] = [0, 0, 0]

output_img = Image.fromarray(output_array)

plt.figure(figsize=(6, 6))
plt.imshow(output_img)
plt.axis("off")
plt.savefig('out.png')
