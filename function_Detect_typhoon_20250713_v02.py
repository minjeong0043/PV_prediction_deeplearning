# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 00:45:36 2025

@author: minjeong
"""

# import library
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
import matplotlib.patches as patches



# Define function

# Select brightest region
def find_brightest_blob(mask, header_height=12):
    # 헤더 영역 제외 (복사본 사용)
    masked = mask.copy()
    masked[:header_height, :] = 0  # 상 단 헤더 제거

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(masked, connectivity=8)
    areas = stats[1:, cv2.CC_STAT_AREA]
    if len(areas) == 0:
        return (0, 0), None  # 중심 좌표, ROI 좌표 없음

    max_index = np.argmax(areas) + 1
    center = tuple(centroids[max_index].astype(int))

    # ROI 좌표 계산
    cx, cy = center
    x = max(cx - roi_size // 2, 0)
    y = max(cy - roi_size // 2, 0)
    x = min(x, mask.shape[1] - roi_size)
    y = min(y, mask.shape[0] - roi_size)

    return center, (x, y, roi_size, roi_size)

def find_brightest_blob_v2(bright_mask, header_height=100):
    masked = bright_mask.copy()
    masked[:header_height, :] = 0
    # 여기서 이전 값과 거리있는 픽셀 지우면 될 듯 위에 코드 처럼

    # 해당 roi 영역의 값들의 합이 특정 threshold보다 커야 태풍으로 인식
    thresh_roi = 46000
    roi_size = 38

    centers = []  # 중심점 저장 리스트
    rois = []     # ROI 좌표 저장 리스트 (필요 시)

    while True:        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(masked, connectivity=8)
        areas = stats[1:, cv2.CC_STAT_AREA]
        
        if len(areas) == 0:
            break  # 더 이상 남은 성분 없음
        
        max_index = np.argmax(areas) + 1
        center = tuple(centroids[max_index].astype(int))
        
        # ROI 추출
        # print(f"prev_center: {center}")
        cx, cy = center
        # print(f"post_center: {center}")
        x = int(max(cx - roi_size // 2, 0))
        y = int(max(cy - roi_size // 2, 0))
        x = int(min(x, masked.shape[1] - roi_size))
        y = int(min(y, masked.shape[0] - roi_size))
        roi = (x, y, roi_size, roi_size)
        sum_roi = 0
        sum_roi = np.sum(masked[y:y+roi_size, x:x+roi_size])
        # print(f"sum_roi: {sum_roi}")
        
        # plt.imshow(masked, cmap='gray')
        # rect = patches.Rectangle((x, y), roi_size, roi_size, linewidth=2, edgecolor='r', facecolor='none')
        # plt.gca().add_patch(rect)
        # plt.scatter(cx, cy, c='blue', s=100)
        # plt.show()
        if sum_roi >= thresh_roi:
            centers.append(center)
            # print(f"center : {center}")
            rois.append((x, y, roi_size, roi_size))
            # print(f"x, y : {x, y}")
            # 해당 영역 제거 → 다음 중심 찾기 위해
            x, y, w, h = roi
            masked[y:y+h, x:x+w] = 0
            masked = masked.copy()  # 업데이트된 마스크로 새로 연결 성분 추출
        else:
            # 너무 약하면 제거하고 다음으로
            masked[y:y+roi_size, x:x+roi_size] = 0
            masked = masked.copy()
            continue
        
    return centers, rois

# Exploration eye of typhoon
def find_eye_region_v2(gray_img, center, search_radius=70 * (128/2665), dark_threshold=190, refine_radius=5 * (128/2665)):
    """
    개선된 눈 찾기 함수
    :param gray_img: 흑백 이미지 (numpy array)
    :param center: (x, y) 튜플, 밝은 blob 중심
    :param search_radius: 탐색 반경 (픽셀)
    :param dark_threshold: 눈 후보가 되기 위한 최대 밝기값
    :param refine_radius: 최저밝기 위치를 기준으로 재검토할 반경 (픽셀)
    :return: (x, y) 눈 후보 좌표 또는 None
    """
    cx, cy = center
    h, w = gray_img.shape

    x_start = max(cx - search_radius, 0)
    x_end = min(cx + search_radius + 1, w)
    y_start = max(cy - search_radius, 0)
    y_end = min(cy + search_radius + 1, h)

    search_area = gray_img[y_start:y_end, x_start:x_end]

    min_val = np.min(search_area)
    min_pos = np.unravel_index(np.argmin(search_area), search_area.shape)

    # 탐색 영역 내 최저값 위치 좌표 (원본 이미지 기준)
    eye_x = x_start + min_pos[1]
    eye_y = y_start + min_pos[0]

    # 최저값 위치 주변 영역 재검토 (refine_radius 만큼의 작은 박스)
    rx_start = max(eye_x - refine_radius, 0)
    rx_end = min(eye_x + refine_radius + 1, w)
    ry_start = max(eye_y - refine_radius, 0)
    ry_end = min(eye_y + refine_radius + 1, h)

    refine_area = gray_img[ry_start:ry_end, rx_start:rx_end]
    refine_mean = np.mean(refine_area)

    # 어두움 판단 기준 : 주변 평균 밝기가 dark_threshold 이하일 때만 눈으로 인정
    if refine_mean > dark_threshold:
        return None

    # 눈 후보 위치 반환
    return (eye_x, eye_y)

def find_eye_region_v3(gray_img, centers, search_radius=68 * (128/2665), dark_threshold=190, refine_radius=10 * (128/2665), roi_size = 38):
    eyes = [None] * len(centers)
    for i in range(len(centers)):
        print(i)
        center = centers[i]
        cx, cy = center
        h, w = gray_img.shape
        
        x_start = int(max(cx - search_radius, 0))
        x_end = int(min(cx + search_radius, w))
        y_start = int(max(cy - search_radius, 0))
        y_end = int(min(cy + search_radius, h))
        
        search_area = gray_img[y_start:y_end, x_start:x_end]
        
        min_val = np.min(search_area)
        min_pos = np.unravel_index(np.argmin(search_area), search_area.shape)
        
        eye_x = x_start + min_pos[1]
        eye_y = y_start + min_pos[0]
        
        # 최저값 위치 주변 영역 재검토 (refine_rdius 만큼의 작은 박스)
        rx_start = int(max(eye_x - refine_radius, 0))
        rx_end = int(min(eye_x + refine_radius + 1, w))
        ry_start = int(max(eye_y - refine_radius, 0))
        ry_end = int(min(eye_y + refine_radius + 1, h))
        
        refine_area = gray_img[ry_start:ry_end, rx_start:rx_end]
        refine_mean = np.mean(refine_area)
        
        # 어두움 판단 기준: 주변 평균 밝기가 dark_threshold 이하일 때만 눈으로 인정
        # 추가로... 눈은 흰 값들의 둘러싸여있어야함.
        if refine_mean < dark_threshold:
            eyes[i] = ((eye_x, eye_y))

    print(eyes)

    centers_fin = [None] * len(centers)
    for i in range(len(centers)):
        if eyes[i] is not None:
            centers_fin[i] = eyes[i]
        else:
            centers_fin[i] = centers[i]
            
    # print(f"centers_fin : {centers_fin}")
    
    return centers_fin

def plot_bright_blob(gray_img, center1=None, center2=None, roi1=None, roi2=None):
    plt.figure(figsize=(10, 10))
    plt.imshow(gray_img, cmap='gray')

    # 첫 번째 중심, ROI
    if center1 is not None:
        if center1 != (0, 0):
            plt.scatter(*center1, s=120, c='orange', marker='*', label='Typhoon Center 1')
            x, y, w, h = roi1
            plt.gca().add_patch(
                plt.Rectangle((x, y), w, h, edgecolor='orange', facecolor='none', linewidth=2, linestyle='--'))
            print("첫 번째 태풍 중심:", center1)

    # 두 번째 중심, ROI
    if center2 is not None:
        if center2 != (0, 0):
            plt.scatter(*center2, s=120, c='cyan', marker='*', label='Typhoon Center 2')
            x, y, w, h = roi2
            plt.gca().add_patch(
                plt.Rectangle((x, y), w, h, edgecolor='cyan', facecolor='none', linewidth=2, linestyle='--'))
            print("두 번째 태풍 중심:", center2)

    plt.title("Detected Multiple Typhoon Centers")
    # plt.legend(loc='upper left')
    plt.axis('off')
    plt.show()

def Detect_typhoon_center(img_path, index):
    # img_path = r"\\Ugrid\sml_nas\연구용데이터\태풍이미지\Imag_typhoon\10.하이선_(전처리, 누락데이터)\gk2a_ami_le1b_ir087_ea020lc_202009011200.png"

    gray_img = np.array(Image.open(img_path).convert("L"))
    img_resized = gray_img.resize((128, 128))
    gray_img = np.array(img_resized)
    
    # bright mask param
    header_height = 12
    percentile = 97
    thresh_val = np.percentile(gray_img, percentile)

    roi_size = 38

    ## Select ROI
    # img1
    bright_mask = (gray_img >= thresh_val).astype(np.uint8) * 255
    # center1_1, roi1_1 = find_brightest_blob(bright1_mask)

    # if roi1_1 is not None:
    #     x, y, w, h = roi1_1
    #     bright1_mask[y:y + h, x:x + w] = 0
    # center1_2, roi1_2 = find_brightest_blob(bright1_mask)
    centers, rois = find_brightest_blob_v2(bright_mask)

    ## 표적 내의 태풍 눈 구하기
    # eye1_1 = find_eye_region_v2(gray1_img, center1_1)
    # eye1_2 = find_eye_region_v2(gray1_img, center1_2)

    # center1_1_fin = np.zeros(2)
    # center1_2_fin = np.zeros(2)

    # # img 1
    # if eye1_1 is not None:
    #     center1_1_fin = np.array(eye1_1)
    # else:
    #     center1_1_fin = np.array(center1_1)

    # if eye1_2 is not None:
    #     center1_2_fin = np.array(eye1_2)
    # else:
    #     center1_2_fin = np.array(center1_2)
    centers_fin = find_eye_region_v3(gray_img, centers)

    # # print each center
    # print("center1_1fin : ", center1_1_fin, "center1_2fin : ", center1_2_fin)

    # plt.figure(figsize=(10, 10))
    # plt.imshow(gray1_img, cmap='gray')
    # # 첫 번째 중심, ROI
    # plt.scatter(*center1_1_fin, s=120, c='orange', marker='*', label='Typhoon Center 1')
    # x, y, w, h = roi1_1
    # plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor='orange', facecolor='none', linewidth=2, linestyle='--'))

    # plt.scatter(*center1_2_fin, s=120, c='cyan', marker='*', label='Typhoon Center 2')
    # x, y, w, h = roi1_2
    # plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor='cyan', facecolor='none', linewidth=2, linestyle='--'))

    # plt.title(f"Index-{index} /Detected Multiple Typhoon Centers")
    # plt.legend(loc='upper left')
    # plt.axis('off')
    # plt.show()

    # 중심 추정 실패 시 기본값 처리
    # if center1_1_fin is None or center1_2_fin is None:
    #     print(f"[WARNING] Eye or blob not detected in: {img1_path}")
    #     return None, None
    
    # plt.figure()
    # plt.imshow(gray_img, cmap='gray')
    # color = ['red', 'orange', 'blue']
    # for i in range(len(centers)):
    #     plt.scatter(*centers_fin[i], s=120, c = color[i], marker='*', label=f'Typhoon Center {i+1}')
    #     x, y, w, h = rois[i]
    #     plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor=color[i], facecolor='none', linewidth=2, linestyle='--'))
        
    # plt.title("Detected Multiple Typhoon Centers")
    # plt.legend(loc='upper left')
    # plt.axis('off')
    # plt.show()
    return centers_fin, rois

def Detect_typhoon_center_v2(img_path, index, prev_roi = None):
    # img_path = r"\\Ugrid\sml_nas\연구용데이터\태풍이미지\Imag_typhoon\10.하이선_(전처리, 누락데이터)\gk2a_ami_le1b_ir087_ea020lc_202009011200.png"
    gray_img = Image.open(img_path).convert("L")
    img_resized = gray_img.resize((128, 128))
    gray_img = np.array(img_resized)

    # 헤더 제외하기
    # header_height = 100 # Original Img
    header_height = 12
    percentile = 97.0
    thresh_val = np.percentile(gray_img, percentile)

    # ROI(Region of Interest)

    # 밝기 마스크(밝은 곳 집중되어 있으면 태풍으로 인식)
    bright_mask = (gray_img >= thresh_val).astype(np.uint8) * 255

    # plt.figure
    # plt.imshow(bright_mask)
    # plt.show()

    # ------------------------------------------------------
    # 밝은 곳 중심 구하기
    # ------------------------------------------------------
    masked = bright_mask.copy()
    masked[:header_height, :] = 0
    # 여기서 이전 값과 거리있는 픽셀 지우면 될 듯 위에 코드 처럼

    # 해당 roi 영역의 값들의 합이 특정 threshold보다 커야 태풍으로 인식
    # thresh_roi = 15613000
    # roi_size = 800
    # thresh_roi = 7230525
    thresh_roi = 35600
    roi_size = 38
    centers = []  # 중심점 저장 리스트
    rois = []     # ROI 좌표 저장 리스트 (필요 시)

    # prev_rois = [(2185, 1865, 800, 800), (82, 1619, 800, 800)]
    # update_prev_rois = [(x, y, 1000, 1000) for (x, y, w, h) in prev_rois]
    while True:        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(masked, connectivity=8)
        areas = stats[1:, cv2.CC_STAT_AREA]
        
        if len(areas) == 0:
            break  # 더 이상 남은 성분 없음
        
        max_index = np.argmax(areas) + 1
        center = tuple(centroids[max_index].astype(int))
        
        # ROI 추출
        # print(f"prev_center: {center}")
        cx, cy = center
        # print(f"post_center: {center}")
        x = max(cx - roi_size // 2, 0)
        y = max(cy - roi_size // 2, 0)
        x = min(x, masked.shape[1] - roi_size)
        y = min(y, masked.shape[0] - roi_size)
        roi = (x, y, roi_size, roi_size)
        sum_roi = 0
        sum_roi = np.sum(masked[y:y+roi_size, x:x+roi_size])
        # print(f"sum_roi: {sum_roi}")
        
        # plt.imshow(masked, cmap='gray')
        # rect = patches.Rectangle((x, y), roi_size, roi_size, linewidth=2, edgecolor='r', facecolor='none')
        # plt.gca().add_patch(rect)
        # plt.scatter(cx, cy, c='blue', s=100)
        # plt.show()
        if sum_roi >= thresh_roi:
            centers.append(center)
            # print(f"center : {center}")
            rois.append((x, y, roi_size, roi_size))
            print(f"x, y : {x, y}")
            # 해당 영역 제거 → 다음 중심 찾기 위해
            x, y, w, h = roi
            masked[y:y+h, x:x+w] = 0
            masked = masked.copy()  # 업데이트된 마스크로 새로 연결 성분 추출
        else:
            # 너무 약하면 제거하고 다음으로
            masked[y:y+roi_size, x:x+roi_size] = 0
            masked = masked.copy()
            continue

    print(f"centers : {centers}")
    # --------------------------------------------------------
    # 태풍 눈 구하기
    # --------------------------------------------------------
    search_radius = 3
    dark_threshold = 190
    refine_radius = 1
    eyes = [None] * len(centers)
    for i in range(len(centers)):
        print(i)
        center = centers[i]
        cx, cy = center
        h, w = gray_img.shape
        
        x_start = int(max(cx - search_radius, 0))
        x_end = int(min(cx + search_radius, w))
        y_start = int(max(cy - search_radius, 0))
        y_end = int(min(cy + search_radius, h))
        
        search_area = gray_img[y_start:y_end, x_start:x_end]
        
        min_val = np.min(search_area)
        min_pos = np.unravel_index(np.argmin(search_area), search_area.shape)
        
        eye_x = x_start + min_pos[1]
        eye_y = y_start + min_pos[0]
        
        # 최저값 위치 주변 영역 재검토 (refine_rdius 만큼의 작은 박스)
        rx_start = int(max(eye_x - refine_radius, 0))
        rx_end = int(min(eye_x + refine_radius + 1, w))
        ry_start = int(max(eye_y - refine_radius, 0))
        ry_end = int(min(eye_y + refine_radius + 1, h))
        
        refine_area = gray_img[ry_start:ry_end, rx_start:rx_end]
        refine_mean = np.mean(refine_area)
        
        # 어두움 판단 기준: 주변 평균 밝기가 dark_threshold 이하일 때만 눈으로 인정
        # 추가로... 눈은 흰 값들의 둘러싸여있어야함.
        if refine_mean < dark_threshold:
            eyes[i] = ((eye_x, eye_y))

    print(eyes)

    centers_fin = [None] * len(centers)
    for i in range(len(centers)):
        if eyes[i] is not None:
            centers_fin[i] = eyes[i]
        else:
            centers_fin[i] = centers[i]
            
    print(f"centers_fin : {centers_fin}")

    # plt.figure()
    # plt.imshow(gray_img, cmap='gray')
    # color = ['red', 'orange', 'blue']
    # for i in range(len(centers)):
    #     plt.scatter(*centers_fin[i], s=120, c = color[i], marker='*', label=f'Typhoon Center {i+1}')
    #     x, y, w, h = rois[i]
    #     plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor=color[i], facecolor='none', linewidth=2, linestyle='--'))
        
    # plt.title("Detected Multiple Typhoon Centers")
    # plt.legend(loc='upper left')
    # plt.axis('off')
    # plt.show()
    
    return centers_fin, rois

def Detect_typhoon_center_withPrev(img_path, index, prev_centers_fin):
    gray_img = Image.open(img_path).convert("L")
    img_resized = gray_img.resize((128, 128))
    gray_img = np.array(img_resized)

    header_height = 12
    percentile = 97.0
    thresh_val = np.percentile(gray_img, percentile)

    # 밝기 마스크(밝은 곳 집중되어 있으면 태풍으로 인식)
    bright_mask = (gray_img >= thresh_val).astype(np.uint8) * 255


    # ------------------------------------------------------
    # 밝은 곳 중심 구하기
    # ------------------------------------------------------
    masked = bright_mask.copy()
    masked[:header_height, :] = 0

    thresh_roi = 35600
    roi_size = 38
    centers = []  # 중심점 저장 리스트
    rois = []     # ROI 좌표 저장 리스트 (필요 시)


    for i in range(len(prev_centers_fin)):
        # 이전 center 중심으로 마스크 재수정
        center = prev_centers_fin[i]
        centers_masked = masked.copy()
        centers_masked[:, :] = 0
        
        roi_size_center = 50
        
        cx, cy = center
        half = roi_size_center // 2
        y1 = max(0, cy - half)
        y2 = min(centers_masked.shape[0], cy+half)
        x1 = max(0, cx - half)
        x2 = min(centers_masked.shape[1], cx+half)
        
        centers_masked[y1:y2, x1:x2] = masked[y1:y2, x1:x2]
        # plt.figure()
        # plt.imshow(centers_masked)
        # plt.show()
        
        #출력은 centers_masked
        while True:        
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(centers_masked, connectivity=8)
            areas = stats[1:, cv2.CC_STAT_AREA]
            
            if len(areas) == 0:
                break  # 더 이상 남은 성분 없음
            
            max_index = np.argmax(areas) + 1
            center = tuple(centroids[max_index].astype(int))
            
            # ROI 추출
            # print(f"prev_center: {center}")
            cx, cy = center
            # print(f"post_center: {center}")
            x = max(cx - roi_size // 2, 0)
            y = max(cy - roi_size // 2, 0)
            x = min(x, centers_masked.shape[1] - roi_size)
            y = min(y, centers_masked.shape[0] - roi_size)
            roi = (x, y, roi_size, roi_size)
            sum_roi = 0
            sum_roi = np.sum(centers_masked[y:y+roi_size, x:x+roi_size])
            print(f"sum_roi: {sum_roi}")
            
            # plt.imshow(centers_masked, cmap='gray')
            # rect = patches.Rectangle((x, y), roi_size, roi_size, linewidth=2, edgecolor='r', facecolor='none')
            # plt.gca().add_patch(rect)
            # plt.scatter(cx, cy, c='blue', s=100)
            # plt.show()
            if sum_roi >= thresh_roi:
                centers.append(center)
                # print(f"center : {center}")
                rois.append((x, y, roi_size, roi_size))
                print(f"x, y : {x, y}")
                # 해당 영역 제거 → 다음 중심 찾기 위해
                x, y, w, h = roi
                centers_masked[y:y+h, x:x+w] = 0
                centers_masked = centers_masked.copy()  # 업데이트된 마스크로 새로 연결 성분 추출
            else:
                # 너무 약하면 제거하고 다음으로
                centers_masked[y:y+roi_size, x:x+roi_size] = 0
                centers_masked = centers_masked.copy()
                continue

    print(f"centers : {centers}")
    # --------------------------------------------------------
    # 태풍 눈 구하기
    # --------------------------------------------------------
    search_radius = 3
    dark_threshold = 190
    refine_radius = 1
    eyes = [None] * len(centers)
    for i in range(len(centers)):
        print(i)
        center = centers[i]
        cx, cy = center
        h, w = gray_img.shape
        
        x_start = int(max(cx - search_radius, 0))
        x_end = int(min(cx + search_radius, w))
        y_start = int(max(cy - search_radius, 0))
        y_end = int(min(cy + search_radius, h))
        
        search_area = gray_img[y_start:y_end, x_start:x_end]
        
        min_val = np.min(search_area)
        min_pos = np.unravel_index(np.argmin(search_area), search_area.shape)
        
        eye_x = x_start + min_pos[1]
        eye_y = y_start + min_pos[0]
        
        # 최저값 위치 주변 영역 재검토 (refine_rdius 만큼의 작은 박스)
        rx_start = int(max(eye_x - refine_radius, 0))
        rx_end = int(min(eye_x + refine_radius + 1, w))
        ry_start = int(max(eye_y - refine_radius, 0))
        ry_end = int(min(eye_y + refine_radius + 1, h))
        
        refine_area = gray_img[ry_start:ry_end, rx_start:rx_end]
        refine_mean = np.mean(refine_area)
        
        # 어두움 판단 기준: 주변 평균 밝기가 dark_threshold 이하일 때만 눈으로 인정
        # 추가로... 눈은 흰 값들의 둘러싸여있어야함.
        if refine_mean < dark_threshold:
            eyes[i] = ((eye_x, eye_y))

    print(eyes)

    centers_fin = [None] * len(centers)
    for i in range(len(centers)):
        if eyes[i] is not None:
            centers_fin[i] = eyes[i]
        else:
            centers_fin[i] = centers[i]
            
    print(f"centers_fin : {centers_fin}")

    # plt.figure()
    # plt.imshow(gray_img, cmap='gray')
    # color = ['red', 'orange', 'blue']
    # for i in range(len(centers)):
    #     plt.scatter(*centers_fin[i], s=120, c = color[i], marker='*', label=f'Typhoon Center {i+1}')
    #     x, y, w, h = rois[i]
    #     plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor=color[i], facecolor='none', linewidth=2, linestyle='--'))
        
    # plt.title("Detected Multiple Typhoon Centers")
    # plt.legend(loc='upper left')
    # plt.axis('off')
    # plt.show()
    
    return centers_fin, rois

def plot_final_Image(img_path, outputpath, centers_fin, rois, index):
    gray_img = Image.open(img_path).convert("L")
    img_resized = gray_img.resize((128, 128))
    gray_img = np.array(img_resized)
    
    plt.figure()
    plt.imshow(gray_img, cmap='gray')
    color = ['red', 'orange', 'blue']
    for i in range(len(centers_fin)):
        plt.scatter(*centers_fin[i], s=120, c = color[i], marker='*', label=f'Typhoon Center {i+1}')
        x, y, w, h = rois[i]
        plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor=color[i], facecolor='none', linewidth=2, linestyle='--'))
        
    plt.title(f"{index} / Detected Multiple Typhoon Centers")
    plt.legend(loc='upper left')
    plt.axis('off')
    plt.savefig(outputpath)
    plt.show()
    
    
def match_centers(prev_centers, curr_centers, max_distance=50):
    """
    이전 중심과의 거리 기반으로 가장 가까운 현재 중심을 매칭.
    max_distance: 허용 가능한 최대 거리 (픽셀)
    """
    if prev_centers is None or curr_centers is None:
        return curr_centers

    matched = [None] * len(prev_centers)
    used = set()

    for i, prev in enumerate(prev_centers):
        min_dist = float('inf')
        min_idx = -1
        for j, curr in enumerate(curr_centers):
            if j in used:
                continue
            dist = np.linalg.norm(np.array(prev) - np.array(curr))
            if dist < min_dist:
                min_dist = dist
                min_idx = j

        # 거리 임계값 초과 시 None으로 간주
        if min_dist <= max_distance:
            matched[i] = curr_centers[min_idx]
            used.add(min_idx)
        else:
            print(f"[경고] prev_center {i} 와 매칭된 대상 없음 (거리 {min_dist:.1f} > {max_distance})")

    return matched
