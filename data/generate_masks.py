import os

import numpy as np
from PIL import Image

files = os.listdir("raspi/mask")
for file in files:
    img = np.asarray(Image.open(f"raspi/mask/{file}").convert("RGB")).mean(2)
    binarized_img = np.where(img > 0, 255, 0).astype(np.uint8)
    result_img = Image.fromarray(binarized_img)
    result_img.save(f"raspi/mask/{file}")
