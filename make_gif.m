clc; clear all; close all; 

folder = 'O:\code_250217\predict1hmodel(latent64, input128)\predict1h_Epoch9';
files = dir(fullfile(folder, '*.png'));

files = {files.name};

outputFile = 'output.gif';

[A, map] = rgb2ind(imread(files{1}), 256);
imwrite(A, map, outputFile, 'GIF', 'LoopCount',Inf, 'DelayTime',0.5);

for i = 2:length(files)
    [A, map] = rgb2ind(imread(files{i}), 256);
    imwrite(A, map, outputFile, 'GIF', 'WriteMode', 'append', 'DelayTime', 0.5);
end
disp('GIF 저장')