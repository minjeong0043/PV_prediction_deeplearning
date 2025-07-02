function [wind_speed, wind_dir] = WindSpeedDir(img1_path, img2_path, img3_path, x, y)

    % Load images
    img1 = im2double(rgb2gray(imread(img1_path)));
    img2 = im2double(rgb2gray(imread(img2_path)));
    img3 = im2double(rgb2gray(imread(img3_path)));

    % 1→2 optical flow
    [dx12, dy12] = OpticalFlow(img1, img2);
    [wind_speed12, wind_dir12] = convertDeltaToKmDeg(dx12, dy12, x, y);

    % 2→3 optical flow
    [dx23, dy23] = OpticalFlow(img2, img3);
    [wind_speed23, wind_dir23] = convertDeltaToKmDeg(dx23, dy23, x, y);

    % 평균
    wind_speed = (wind_speed12 + wind_speed23) / 2;
    wind_dir = (wind_dir12 + wind_dir23) / 2;

end

function [dx, dy] = OpticalFlow(img1, img2)
    % Farneback optical flow (MATLAB Computer Vision Toolbox)
    opticFlow = opticalFlowFarneback('NumPyramidLevels',3, ...
                                     'PyramidScale',0.5, ...
                                     'NumIterations',3, ...
                                     'NeighborhoodSize',15, ...
                                     'FilterSize',5);
    % 첫 프레임 초기화
    estimateFlow(opticFlow, img1);
    % 두번째 프레임
    flow = estimateFlow(opticFlow, img2);
    
    dx = flow.Vx;
    dy = flow.Vy;
end

function [wind_speed, wind_dir] = convertDeltaToKmDeg(dx, dy, x, y)
    % flow에서 특정 좌표 벡터
    u_pixel = dx(y, x);  % y행 x열
    v_pixel = dy(y, x);

    % Python에서 pixel_size=1km, 10분(600초) 사용
    pixel_size_m = 1000;    % 1 pixel = 1km
    dt_sec = 60*10;         % 10분 간격

    u_mps = u_pixel * pixel_size_m / dt_sec;
    v_mps = v_pixel * pixel_size_m / dt_sec;

    wind_speed = hypot(u_mps, v_mps);
    wind_dir = atan2d(v_mps, u_mps);
    if wind_dir < 0
        wind_dir = wind_dir + 360;
    end
end
