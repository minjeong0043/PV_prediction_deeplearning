clc; clear all; close all;
load('dlnetGenerator_ir(inputSize128, latentvector256, dongAsia, Epoch50)', 'dlnetGenerator');

numLatentInputs = 256;
z = randn(1, 1, numLatentInputs, 144, 'single');
dlZ = dlarray(z, 'SSCB');
dlXGenerated = predict(dlnetGenerator, dlZ);
dlX = extractdata(dlXGenerated);
size(dlX(:,:,:,1))

h = figure;
imshow(dlX(:,:,:,1))
h = figure;
I = imtile(dlX);
I_rescale = rescale(I);
image(I_rescale);
title('Generated Images');

% outputFolder = '';
% saveas(h, fullfile(outputFolder, 'CheckingGenerator.png'));
saveas(h, 'CheckingGenerator.png');
close(h)

z_forPlot = squeeze(z)
size(z_forPlot(:,1))
k = figure;
scatter(1:256, z_forPlot(:,1), "filled")
xlim([0, 256])
size(squeeze(z))

p = figure;
for i = 1:12:12
    subplot(12, 12, i)
    scatter(1:256, z_forPlot(:,i), "filled")
    title([' index : ', string(i)])
end

p = figure;
img_index = 1;
z_index = 1;
for i = 1:12*24
   subplot(12,24, i);
   if mod(i, 2) == 1
       imshow(dlX(:,:,:,img_index))
       axis off
       title(['z_index : ', num2str(img_index)])
   else
       scatter(1:256, z_forPlot(:,1), "filled")
       title(['img index : ', num2str(img_index)])
       img_index = img_index + 1;
   end
end

p = figure;

numRows = 12; % 서브플롯 행 개수
numCols = 24; % 서브플롯 열 개수 (12x2 = 한 세트)
totalPlots = numRows * numCols; % 총 서브플롯 개수

img_index = 1;

for i = 1:totalPlots
   subplot(numRows, numCols, i);
   
   if mod(i, 2) == 1  % 홀수 번째는 imshow
       imshow(dlX(:,:,:,img_index));
       title(['Image Index: ', num2str(img_index)]);
   else  % 짝수 번째는 scatter
       scatter(1:256, z_forPlot(:,img_index), "filled");
       title(['Scatter Index: ', num2str(img_index)]);
       img_index = img_index + 1; % 한 세트가 끝날 때만 증가
   end
end


img = figure;
for i = 1:12*12
    subplot(12, 12, i);
    imshow(dlX(:,:,:,i));
    axis off
end

z = figure;
for i = 1:12*12
    subplot(12, 12, i);
    scatter(1:256, z_forPlot(:,i), "filled");
end


montage(dlX, 'Size', [12 12]);

z = figure;
tiledlayout(12,12, 'TileSpacing', 'none', 'Padding', 'none');
for i = 1:12*12
    nexttile;
    scatter(1:256, z_forPlot(:,i), "filled");
    axis off;
end
