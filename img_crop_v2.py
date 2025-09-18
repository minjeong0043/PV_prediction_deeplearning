#적외선 8.7um:65
import os
import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np

# GPU 사용 여부 확인
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# if device.type != "cuda":
#     raise RuntimeError("GPU XX")
# print(f"Using device: {device}")

# 입력 및 출력 폴더 경로 설정
folder = r"\\Ugrid\sml_nas\연구용데이터\위성이미지\천리안2호_적외(구름상)_2020_10min"
outputFolder = r"\\Ugrid\sml_nas\연구용데이터\위성이미지\천리안2호_적외(구름상)_HeaderCrop\천리안2호_적외(구름상)_2020_10min"
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# 파일 목록 가져오기
files = os.listdir(folder)
files_array = np.array(files)
sorted_files = np.sort(files_array)
print(f"총 {len(sorted_files)}개의 파일이 발견")

# 특정 파일부터 시작 (예: 'gk2a_ami_le1b_ir087_ko020lc_202409120550.png')
# index_2 = np.where(files_array == 'gk2a_ami_le1b_ir087_ko020lc_202409190820.png')[0][0]
# missingFile_index = np.where(sorted_files == 'gk2a_ami_le1b_ir087_ea020lc_202104111900.png')[0][0]
# 이미지 처리 루프
for i in range(1, len(sorted_files)):
    file_name = sorted_files[i]
    path = os.path.join(folder, file_name)
    output_path = os.path.join(outputFolder, file_name)

    # 이미지 열기 및 텐서 변환
    image = Image.open(path)
    to_tensor = T.ToTensor()
    image_tensor = to_tensor(image).to(device)

    cropped_tensor = image_tensor[:, 65:, : ]
    # resize_transform = T.Resize((image.height, image.width))
    # resized_tensor = resize_transform(cropped_tensor)

    # 텐서를 PIL 이미지로 변환 후 저장 (CPU로 이동 필요)
    to_pil = T.ToPILImage()
    resized_image = to_pil(cropped_tensor.cpu())
    resized_image.save(output_path)

    print(f"{i + 1}/{len(sorted_files)}: {file_name} 처리 완료")

print("모든 이미지 처리가 완")
