# 폴더 내 파일들에 대해서 winds Speed & Direction
import matplotlib.pyplot as plt
import numpy as np
from OpticalFlow_Function_250701 import WindSpeedDir
import os
from PIL import Image
import pandas as pd

folder_path = r'D:\천리안2호_적외(구름상)_2022~2023_10min_crop'
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')]) # 폴더 내 파일 리스트
# print(file_list)

# 고산 지역 좌표 (33.294, 126.163)-->(1509.54, 1621.61)
gosan_x = int(1509.54)
gosan_y = int(1595.5) #이미지 전처리 고려한 좌표값 산출
# 합천 지역 좌표 (35.565, 128.17) -->(1596.78, 1495.79)
hapcheon_x = int(1596.78)
hapcheon_y = int(1466.6)
file_path = os.path.join(folder_path, file_list[0])
img1 = Image.open(file_path)

# plt.figure(figsize=(10, 8))
# plt.imshow(img1)
# plt.scatter([gosan_x, hapcheon_x], [gosan_y, hapcheon_y], c='red', s=80, marker='o', label='Station')
# plt.text(gosan_x +10, gosan_y +10, 'Gosan', color='red', fontsize=12)
# plt.text(hapcheon_x +10, hapcheon_y +10, 'Hapcheon', color='red', fontsize=12)
# plt.legend()
# plt.show()
index = np.arange(2,len(file_list)-1)
# print(index)
wind_speed_excel = []
wind_dir_excel = []
# for i in range(len(file_list) - 2):
for i in range(5):
    files_window = file_list[i:i+3]
    # print(f"window { i} : {files_window}")
    file_path1 = os.path.join(folder_path, file_list[i])
    file_path2 = os.path.join(folder_path, file_list[i+1])
    file_path3 = os.path.join(folder_path, file_list[i+2])

    wind_speed, wind_dir = WindSpeedDir(file_path1, file_path2, file_path3)
    wind_speed_excel.append(wind_speed[gosan_x, gosan_y])
    wind_dir_excel.append(wind_dir[gosan_x, gosan_y])
    print(f"wind Speed : {wind_speed[gosan_x, gosan_y]:.2f}, wind_dir : {wind_dir[gosan_x, gosan_y]:.2f}\n")

# excel로 저장
df1 = pd.DataFrame(index, columns=['Index'])
df2 = pd.DataFrame(wind_speed_excel, columns=['Speed'])
df3 = pd.DataFrame(wind_dir_excel, columns=['Direction'])
merged_df = pd.concat([df1, df2, df3], axis=1)
merged_df.to_excel('wind_from_satelliteImage.xlsx', sheet_name = 'WindData')
