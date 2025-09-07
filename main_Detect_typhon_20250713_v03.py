# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 20:08:13 2025

@author: minjeong
"""

import os
import glob
from function_Detect_typhoon_20250713_v02 import Detect_typhoon_center_v2, plot_final_Image, Detect_typhoon_center_withPrev
import time
import pandas as pd

prev_centers = None
curr_centers = None
prev_rois = None
results = []
centers_fin = []
folder = r'C:\Users\Minjeong\Desktop\태풍이미지(2024-2025)\15. 페이파_(전처리, 누락데이터)_crop'
files = glob.glob(os.path.join(folder, '*.png'))

# Define Output Folder to save output Images
outputFolder = r'C:\Users\Minjeong\Desktop\태풍이미지(2024-2025)\15. 페이파_태풍경로(원본)'
if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)
    
for i, file in enumerate(files):
    try:
        print(f"[{i + 1}/{len(files)}] Processing: {file}")
        # 여기에 이전 center가 있으면 해당 내용 반영하도록
        if prev_centers is None and prev_rois is None:
            centers_fin, rois = Detect_typhoon_center_v2(file, i)
        else:
            centers_fin, rois = Detect_typhoon_center_withPrev(file, i, prev_centers)
            

        # 업데이트
        if centers_fin and rois:
            print('exist center_fin, rois')
            prev_centers = centers_fin
            prev_rois = rois

    except Exception as e:
        print(f"[ERROR] Failed to process {file}: {e}")
        centers_fin = prev_centers
        rois = prev_rois

    # 👉 저장할 데이터 구성
    record = {'Filename': os.path.basename(file)}
    for j in range(len(centers_fin)):
        center = centers_fin[j] if centers_fin else None
        if center is not None:
            record[f'Center{j+1}_X'] = center[0]
            record[f'Center{j+1}_Y'] = center[1]
        else:
            record[f'Center{j+1}_X'] = None
            record[f'Center{j+1}_Y'] = None
    results.append(record)
    
    # Extract file name from path
    filename = os.path.basename(file)
    filepath = os.path.join(outputFolder, filename)
    plot_final_Image(file, filepath, centers_fin, rois, i)
    
# 👉 엑셀로 저장
df = pd.DataFrame(results)
df.to_excel(r'C:\Users\Minjeong\Desktop\태풍이미지(2024-2025)\15. 페이파_태풍경로(원본).xlsx', index=False)
print("[저장 완료] 엑셀에 모든 파일별 중심좌표를 저장했습니다.")