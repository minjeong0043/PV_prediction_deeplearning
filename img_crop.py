import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

# img_path = "D:\mj Kim\위성이미지_적외8.7\구름강조(9-11월, 10분단위)\gk2a_ami_le1b_rgb-cs_ko005lc_202408311500.png"
# image = np.array(Image.open(img_path))
#
# cropped_image = image[90:, :, :]
#
# resized_image = np.array(Image.fromarray(cropped_image).resize((7200, 7200)))
#
# plt.figure(1)
# plt.subplot(1,2,1)
# plt.imshow(image)
# plt.subplot(1,2,2)
# plt.imshow(resized_image)
# plt.axis("off")
# plt.show()

def image_crop(img_path):
    image = np.array(Image.open(img_path))
    cropped_image = image[90:,:,:]
    resized_image = np.array(Image.fromarray(cropped_image).resize((3600,3600)))
    return resized_image


folder = "D:\mj Kim\위성이미지_적외8.7\구름강조(9-11월, 10분단위)"
outputFolder = "D:\mj Kim\위성이미지_적외8.7\구름강조(9-11월, 10분단위)_crop"
os.chdir(folder)
files = os.listdir(folder)
files_array = np.array(files)
print(files_array)
index_2 = np.where(files_array == 'gk2a_ami_le1b_rgb-cs_ko005lc_202411191940.png')[0][0]
print(index_2)
for i in range(index_2, len(files)):
    path = os.path.join(folder, files[i])
    print(path)
    image_c = image_crop(path)
    image_c = Image.fromarray(image_c.astype('uint8'), 'RGB')
    output_path = os.path.join(outputFolder, files[i])
    image_c.save(output_path, 'png')

# image = Image.open(os.path.join(folder, files[1]))
# plt.imshow(image)
# plt.show()

print("cropping fni=")