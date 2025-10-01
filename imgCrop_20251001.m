clc; clear all; close all;

img_path = "\\Ugrid\sml_nas\연구용데이터\위성이미지\천리안2호_적외(구름상)_누락처리\!천리안2호_적외(구름상)_2021_10min";
save_path = "\\Ugrid\sml_nas\연구용데이터\위성이미지\천리안2호_적외(구름상)_누락처리&Crop\천리안2호_적외(구름상)_2021_10min";
if ~exist(save_path)
    mkdir(save_path)
end
i=1;
files = dir(fullfile(img_path, '*.png'));
file_names = {files.name};
for name = file_names
    img = imread(fullfile(img_path, name));
    croppedImage = cropimg(img);
    imwrite(croppedImage, fullfile(save_path, name));
    fprintf('cropped file name(%d/%d) - %s\n', i, length(files), name{1})
    i=i+1;
end

fprintf("++++++++++++++++++++++++++++\nCompleted Cropping\n++++++++++++++++++++++++++++")
%%
function croppedImage = cropimg(img)
    centerX = 1567; centerY = 1441;
    cropSize = 2048;
    
    halfSize = cropSize / 2;
    
    xStart = round(centerX - halfSize + 1);
    xEnd = round(centerX + halfSize);
    yStart = round(centerY - halfSize + 1);
    yEnd = round(centerY + halfSize);
    
    xStart = max(1, xStart);
    yStart = max(1, yStart);
    xEnd = min(size(img, 2), xEnd);
    yEnd = min(size(img, 1), yEnd);
    
    croppedImage = img(yStart:yEnd, xStart:xEnd, :);
end
