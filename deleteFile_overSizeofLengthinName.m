clc; clear all; close all;

folder_path = 'D:\SatelliteImageDownload(10.5color)\2020_1';

% List all image files in the specified folder
imageFiles = dir(fullfile(folder_path, '*.png')); % Adjust the extension as needed
files_name = {imageFiles.name};

for i = 1:length(files_name)
    if length(files_name{i}) > length(files_name{1})
        delete(fullfile(folder_path, files_name{i}))
        fprintf('Delete File : %s\n', files_name{i})
    end
end

disp('Finished Checking')