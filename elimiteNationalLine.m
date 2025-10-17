clc; clear all;

folder = 'C:\Users\minjeong\Desktop\적외선_8.7(2021~2023년, 10분단위)_crop';
% List all image files in the specified folder
imageFiles = dir(fullfile(folder, '*.png'));
imageFiles = {imageFiles.name};

for i = 1: length(imageFiles)
    img_path = fullfile(folder, imageFiles{i});
    EliminateNationalLine(img_path);
    fprintf('(%d / %d) image name : %s\n', i, length(imageFiles), imageFiles{i})
end

%% one file
function EliminateNationalLine(img_path)
% img_path = "C:\Users\minjeong\Desktop\적외선_8.7(2021~2023년, 10분단위)_crop\gk2a_ami_le1b_ir087_ea020lc_202012311500.png";
img = imread(img_path);
img = double(img);
redChannel = img(:, :, 1); 
greenChannel = img(:, :, 2); 
blueChannel = img(:, :, 3);

% 노란색 범위 조건
mask = redChannel >= 121 & greenChannel >= 121 & blueChannel <= 120;
% 노란색 픽셀 검은색으로 일단 대체
img(repmat(mask, [1,1,3])) = 0;

% uint8 변환 후 grayscale 생성
img_uint8 = uint8(img);
img_gray = rgb2gray(img_uint8);

filterSize = 5;
kernel = ones(filterSize);
repeatCount = 10;

for i = 1:repeatCount
    sumImg = conv2(double(img_gray), kernel, 'same');
    centerPixel = double(img_gray);
    neighborSum = sumImg - centerPixel;
    neighborAvg = neighborSum / (filterSize^2 - 1);

    % 대체 대상: 노란색이었던 픽셀 위치 (mask)
    replaceMask = mask;

    % 대체 진행
    img_gray(replaceMask) = neighborAvg(replaceMask);
end

% figure;
% imshow(uint8(img_gray));
% title('Processed Grayscale Image - Yellow Pixels Smoothed');

imwrite(uint8(img_gray), img_path)

end