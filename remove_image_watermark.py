
#图片去灰色水印
import os
import cv2
import numpy as np
from PIL import Image
import shutil

SRC = r"xxxxxxxxxxxxx"
for root, dirs, files in os.walk(SRC):
    print(root)
    num = 20
    for file in files:
        if not file.endswith("jpg") and not file.endswith ("JPG")  and not file.endswith("png"):
            continue
        print(file)
        src = os.path.join(root, file)
        img = cv2.imdecode(np.fromfile(src, dtype=np.uint8), cv2.IMREAD_COLOR)
        # img = cv2.imread(r"xxxxxx\001.jpg")

        alpha = 2.596594846224838
        beta = -161

        new = alpha * img + beta
        new = np.clip(new, 0, 255).astype(np.uint8)

        print(alpha, beta)

        new_path = str(num) + '.png'

        path_list = os.path.splitext(src)
        dst_path = path_list[0] + '_' + str(num) + path_list[1]

        cv2.imwrite(new_path, new)

        img = Image.open(new_path)
        img.save(new_path)
        shutil.move(new_path, dst_path)
        # os.rename(new_path, dst_path)

        num += 1
