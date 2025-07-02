clc; clear; close all;

% 폴더 내 png 파일 불러오기
folder_path = 'D:\천리안2호_적외(구름상)_2022~2023_10min_crop';
file_list_struct = dir(fullfile(folder_path, '*.png'));
file_list = {file_list_struct.name}; 

% 고산 좌표 (픽셀 좌표)
gosan_x = round(1509.54);
gosan_y = round(1621.61);

% 합천 좌표 (사용 안 함)
% hapcheon_x = round(1596.78);
% hapcheon_y = round(1466.6);

% 확인용 샘플 이미지 시각화 (주석 처리)
% img1 = imread(fullfile(folder_path, file_list{1}));
% figure; imshow(img1, []); hold on;
% plot(gosan_x, gosan_y, 'ro', 'MarkerSize', 10, 'LineWidth', 2);
% text(gosan_x+10, gosan_y+10, 'Gosan', 'Color', 'r', 'FontSize', 12);
% hold off;

% index
index = (2:length(file_list)-1)';

% 결과 배열
wind_speed_excel = zeros(length(index), 1);
wind_dir_excel = zeros(length(index), 1);

for i = 1:(length(file_list)-2)
    file1 = fullfile(folder_path, file_list{i});
    file2 = fullfile(folder_path, file_list{i+1});
    file3 = fullfile(folder_path, file_list{i+2});
    
    % OpticalFlow 기반 풍속/풍향 계산
    [wind_speed, wind_dir] = WindSpeedDir(file1, file2, file3, gosan_x, gosan_y);
    
    wind_speed_excel(i) = wind_speed;
    wind_dir_excel(i) = wind_dir;
    
    fprintf('(index %d) wind Speed : %.2f [m/s], wind_dir : %.2f [deg]\n', i, wind_speed, wind_dir);
end

% 엑셀로 저장
filename = 'wind_from_satelliteImage_1.카눈_고산.xlsx';
output_table = table(index, wind_speed_excel, wind_dir_excel, ...
    'VariableNames', {'Index','Speed_mps','Direction_deg'});
writetable(output_table, filename, 'Sheet', 'WindData');

