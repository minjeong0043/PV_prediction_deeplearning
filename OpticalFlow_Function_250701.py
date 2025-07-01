# optical Flow
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from PIL import Image

# 이미지 두 개 받아서 optical Flow 출력하는 코드
def OpticalFlow(img1, img2):
    # Optical Flow 계산 (Lucas-Kanade 방식)
    flow = cv2.calcOpticalFlowFarneback(img1, img2, None,
                                        pyr_scale=0.5, levels=3, winsize=15,
                                        iterations=3, poly_n=5, poly_sigma=1.2, flags=0)

    # flow는 각 픽셀마다 (dx, dy) 벡터 → 풍속 방향
    dx = flow[..., 0]
    dy = flow[..., 1]
    # magnitude, angle = cv2.cartToPolar(dx, dy)

    # 풍속과 풍향 출력
    # wind_speed = magnitude
    # wind_dir = angle * 180 / np.pi  # 각도 (0~360도)
    return dx, dy


def plot_flow(img, dx, dy, title, savefile):
    step = 20
    h, w = img.shape
    y, x = np.mgrid[step // 2:h:step, step // 2:w:step]

    pixel_size_km = 1
    dt_sec = 60 * 20

    u = dx[y, x]
    v = dy[y, x]

    u_mps = u * pixel_size_km * 1000 / dt_sec
    v_mps = v * pixel_size_km * 1000 / dt_sec

    u_mps_smooth = gaussian_filter(u_mps, sigma=2)
    v_mps_smooth = gaussian_filter(v_mps, sigma=2)

    u_resized = cv2.resize(u_mps_smooth, (w, h), interpolation=cv2.INTER_LINEAR)
    v_resized = cv2.resize(v_mps_smooth, (w, h), interpolation=cv2.INTER_LINEAR)

    yy = np.arange(step // 2, h, step)
    xx = np.arange(step // 2, w, step)
    y_sample, x_sample = np.meshgrid(yy, xx, indexing='ij')

    sample_u = u_resized[y_sample, x_sample]
    sample_v = v_resized[y_sample, x_sample]

    plt.figure(figsize=(10, 8))
    plt.imshow(img, cmap='gray', origin='lower')
    plt.quiver(x_sample, y_sample, sample_u, -sample_v, color='red', angles='xy', scale_units='xy', scale=1)
    plt.title(title)
    plt.xlabel("X (pixel)")
    plt.ylabel("Y (pixel)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(savefile, dpi=300)
    plt.show()

# 하나의 figure에 두 개의 flow 비교
def plot_flow_compare(img1, dx1, dy1, title1,
                      img2, dx2, dy2, title2,
                      savefile):
    step = 20
    h, w = img1.shape

    # 첫번째 flow
    y, x = np.mgrid[step // 2:h:step, step // 2:w:step]
    pixel_size_km = 1
    dt_sec = 60 * 20

    u1 = dx1[y, x]
    v1 = dy1[y, x]
    u1_mps = u1 * pixel_size_km * 1000 / dt_sec
    v1_mps = v1 * pixel_size_km * 1000 / dt_sec
    u1_mps_smooth = gaussian_filter(u1_mps, sigma=2)
    v1_mps_smooth = gaussian_filter(v1_mps, sigma=2)
    u1_resized = cv2.resize(u1_mps_smooth, (w, h), interpolation=cv2.INTER_LINEAR)
    v1_resized = cv2.resize(v1_mps_smooth, (w, h), interpolation=cv2.INTER_LINEAR)

    yy = np.arange(step // 2, h, step)
    xx = np.arange(step // 2, w, step)
    y_sample, x_sample = np.meshgrid(yy, xx, indexing='ij')
    sample_u1 = u1_resized[y_sample, x_sample]
    sample_v1 = v1_resized[y_sample, x_sample]

    # 두번째 flow
    u2 = dx2[y, x]
    v2 = dy2[y, x]
    u2_mps = u2 * pixel_size_km * 1000 / dt_sec
    v2_mps = v2 * pixel_size_km * 1000 / dt_sec
    u2_mps_smooth = gaussian_filter(u2_mps, sigma=2)
    v2_mps_smooth = gaussian_filter(v2_mps, sigma=2)
    u2_resized = cv2.resize(u2_mps_smooth, (w, h), interpolation=cv2.INTER_LINEAR)
    v2_resized = cv2.resize(v2_mps_smooth, (w, h), interpolation=cv2.INTER_LINEAR)

    sample_u2 = u2_resized[y_sample, x_sample]
    sample_v2 = v2_resized[y_sample, x_sample]

    # figure
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # 왼쪽: img1
    axes[0].imshow(img1, cmap='gray', origin='lower')
    axes[0].quiver(x_sample, y_sample, sample_u1, -sample_v1, color='red', angles='xy', scale_units='xy', scale=1)
    axes[0].set_title(title1)
    axes[0].set_xlabel("X (pixel)")
    axes[0].set_ylabel("Y (pixel)")
    axes[0].invert_yaxis()

    # 오른쪽: img2
    axes[1].imshow(img2, cmap='gray', origin='lower')
    axes[1].quiver(x_sample, y_sample, sample_u2, -sample_v2, color='red', angles='xy', scale_units='xy', scale=1)
    axes[1].set_title(title2)
    axes[1].set_xlabel("X (pixel)")
    axes[1].set_ylabel("Y (pixel)")
    axes[1].invert_yaxis()

    plt.tight_layout()
    plt.savefig(savefile, dpi=300)
    plt.show()

def WindSpeedDir(img1_path, img2_path, img3_path): # input image path
    img1 = np.array(Image.open(img1_path).convert("L"))
    img2 = np.array(Image.open(img2_path).convert("L"))
    img3 = np.array(Image.open(img3_path).convert("L"))

    dx12, dy12 = OpticalFlow(img1, img2)
    mag12, angle12 = cv2.cartToPolar(dx12, dy12)
    wind_speed12 = mag12
    wind_dir12 = angle12 * 180 / np.pi

    dx23, dy23 = OpticalFlow(img2, img3)
    mag23, angle23 = cv2.cartToPolar(dx23, dy23)
    wind_speed23 = mag23
    wind_dir23 = angle23 * 180 / np.pi

    wind_speed = (wind_speed12 + wind_speed23) / 2
    wind_dir = (wind_dir12 + wind_dir23) / 2

    return wind_speed, wind_dir





