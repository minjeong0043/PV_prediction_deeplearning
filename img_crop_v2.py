# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 22:14:39 2025

@author: minjeong
"""

# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt
# import os
# # 구름강조: 90, 적외선 8.7um: ???
# # img_path = "D:\mj Kim\위성이미지_적외8.7\구름강조(9-11월, 10분단위)\gk2a_ami_le1b_rgb-cs_ko005lc_202408311500.png"
# # image = np.array(Image.open(img_path))
# #
# # cropped_image = image[90:, :, :]
# #
# # resized_image = np.array(Image.fromarray(cropped_image).resize((7200, 7200)))
# #
# # plt.figure(1)
# # plt.subplot(1,2,1)
# # plt.imshow(image)
# # plt.subplot(1,2,2)
# # plt.imshow(resized_image)
# # plt.axis("off")
# # plt.show()
#
# def image_crop(img_path):
#     image = np.array(Image.open(img_path))
#     cropped_image = image[90:,:,:]
#     resized_image = np.array(Image.fromarray(cropped_image).resize((3600,3600)))
#     return resized_image
#
#
# folder = "D:\PV_forecast_2025\적외선_8.7(2021년, 10분단위)"
# outputFolder = "D:\PV_forecast_2025\적외선_8.7(2021년, 10분단위)_crop"
# os.chdir(folder)
# files = os.listdir(folder)
# files_array = np.array(files)
# print(files_array)
# index_2 = np.where(files_array == 'gk2a_ami_le1b_rgb-cs_ko005lc_202411191940.png')[0][0]
# print(index_2)
# for i in range(index_2, len(files)):
#     path = os.path.join(folder, files[i])
#     print(path)
#     image_c = image_crop(path)
#     image_c = Image.fromarray(image_c.astype('uint8'), 'RGB')
#     output_path = os.path.join(outputFolder, files[i])
#     image_c.save(output_path, 'png')
#
# # image = Image.open(os.path.join(folder, files[1]))
# # plt.imshow(image)
# # plt.show()
#
# print("cropping fni=")


#######################
#적외선 8.7um:22
import os
import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np

# GPU 사용 여부 확인

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# if device.type != "cuda":
#     raise RuntimeError("GPU가 감지되지 않았습니다. GPU 환경에서 실행해주세요.")
# print(f"Using device: {device}")

# 입력 및 출력 폴더 경로 설정
folder = r"D:\PV_forecast_2025\적외선_8.7(2021년, 10분단위)"
outputFolder = r"D:\PV_forecast_2025\적외선_8.7(2021년, 10분단위)_crop_v2"
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# 파일 목록 가져오기
files = os.listdir(folder)
files_array = np.array(files)
sorted_files = np.sort(files_array)
print(f"총 {len(sorted_files)}개의 파일이 발견되었습니다.")

# 특정 파일부터 시작 (예: 'gk2a_ami_le1b_ir087_ko020lc_202409120550.png')
# index_2 = np.where(files_array == 'gk2a_ami_le1b_ir087_ko020lc_202409190820.png')[0][0]
missingFile_index = np.where(sorted_files == 'gk2a_ami_le1b_ir087_ea020lc_202104111900.png')[0][0]
# 이미지 처리 루프
for i in range(missingFile_index, len(sorted_files)):
    file_name = sorted_files[i]
    path = os.path.join(folder, file_name)
    output_path = os.path.join(outputFolder, file_name)

    # 이미지 열기 및 텐서 변환
    image = Image.open(path)
    to_tensor = T.ToTensor()
    image_tensor = to_tensor(image).to(device)  # GPU로 이동

    # 상단 22픽셀 크롭 및 리사이즈
    # cropped_tensor = image_tensor[:, 22:, :]
    cropped_tensor = image_tensor[:, 65:, : ]
    resize_transform = T.Resize((image.height, image.width))
    resized_tensor = resize_transform(cropped_tensor)

    # 텐서를 PIL 이미지로 변환 후 저장 (CPU로 이동 필요)
    to_pil = T.ToPILImage()
    resized_image = to_pil(resized_tensor.cpu())  # CPU로 이동 후 PIL 변환
    resized_image.save(output_path)

    print(f"{i + 1}/{len(sorted_files)}: {file_name} 처리 완료")

print("모든 이미지 처리가 완료되었습니다.")
