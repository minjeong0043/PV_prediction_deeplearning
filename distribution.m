clc; clear all;
% 폴더 내 전체 이미지에 대해..
folder = 'C:\Users\leejunwoo\OneDrive - 고려대학교\juan\바탕 화면_준현\mj Kim\위성이미지_적외8.7\구름강조_9';

files = dir(fullfile(folder, '*.png'));

files = natsortfiles({files.name});

img1 = imread(fullfile(folder , files{1}));
if size(img1, 3) == 3
    img1 = rgb2gray(img1);
end

files_length = length(files)

for i = 1:10
    img1 = imread(fullfile(folder , files{i}));
    if size(img1, 3) == 3
        img1 = rgb2gray(img1);
    end
    figure;
    histogram(img1(:), 256, 'Normalization','pdf');
    xlabel('픽셀값');
    ylabel('확률밀도');
    title('이미지의 픽셀 값 분포');
    grid on;
end