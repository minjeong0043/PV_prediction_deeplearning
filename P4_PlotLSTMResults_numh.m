clc; clear all; close all
%% 1) 각 모델별 성능 확인
% prepare dataset and networks
folder = 'D:\PV_forecast_2025\천리안2호_적외(구름상)_2021_10min_crop';
imds = imageDatastore(folder, "IncludeSubfolders",true);
inputSize = [128, 128, 3];
imds = augmentedImageDatastore(inputSize(1:2), imds);

predictNum = 1;
load('dlnetGenerator_ir(inputSize128, latentvector256, dongAsia, Epoch50).mat', 'dlnetGenerator');
load(sprintf('dlnetLSTM_128ir(latentvector256)_PredictTime4h_Epoch60.mat', predictNum), 'dlnetLSTM');

numInputFrames = 3; % 3시간
numTargetFrame = 2; % 2시간

% 미니배치로 데이터 나눔
numFrame = numInputFrames + numTargetFrame;
imds.MiniBatchSize = numFrame;

mbq = minibatchqueue(imds, ...
    'MiniBatchSize', numFrame, ...
    'PartialMiniBatch', 'discard', ...
    'OutputAsDlarray', true);  % false


n = length(imds.Files);
remain = mod(n, numFrame);
numMiniBatchQueue = (n - remain)/numFrame;

i = 1;

mseVals = [];
ssimVals = [];
ofVals = [];
corrVals = [];
% while hasdata(mbq)
while i <100
    dlX = next(mbq); % SSCT dlarray
    %입력만 뽑아내야 함.
    inputData = dlX(:,:,:,1:end-numTargetFrame); % 128*128*3*18
    targetData = dlX(:,:,:,end); %128*128*3
    
    inputData = dlarray(inputData ,"SSCTB");
    targetData = dlarray(targetData, "SSCB");

    lstmOut = predict(dlnetLSTM, inputData);
    lstmOut = dlarray(lstmOut, 'CBSS');

    generatorOut = predict(dlnetGenerator, lstmOut);
    generatorOut = rescale(generatorOut);
    
    targetforPlot = rescale(extractdata(targetData));
    generatorOutforPlot = rescale(extractdata(generatorOut));

    filename = 'difference_animation.gif';
    delayTime = 0.3;  % 프레임 간격 (초)

    p = figure;
    subplot(1,4,1);
    imshow(targetforPlot);
    title('Original Image');
    subplot(1,4,2);
    imshow(generatorOutforPlot);
    title('Predicted Image');
    subplot(1,4,4);
    scatter(1:256, extractdata(squeeze(lstmOut)), "filled");
    xlim([0,256]);
    title('Latent Vector');
    set(p, "Position", [3,511,1914,367]);
    % 이미지의 차이를 시각화
    % 1. 픽셀 단위 차이
    % imshow(imabsdiff(targetforPlot, generatorOutforPlot))
    % title('Pixel Difference');

    % 2. heatmap 기반 차이
    subplot(1,4,3);
    diff_gray = rgb2gray(imabsdiff(targetforPlot, generatorOutforPlot));
    diff_colormap = ind2rgb(im2uint8(mat2gray(diff_gray)), jet(256));
    imshow(diff_colormap);
    title('Heatmap Difference');

    % 3. Alpha Blending
    % alpha = 0.5;
    % blended = imlincomb(alpha, targetforPlot, (1-alpha), generatorOutforPlot);
    % imshow(blended);
    % title('Alpha Blended Image');

    % 4. Edge Detection
    % diff_gray = rgb2gray(imabsdiff(targetforPlot, generatorOutforPlot));
    % bw = imbinarize(diff_gray, 0.1);
    % edges = edge(bw, 'Canny');
    % imshow(targetforPlot)
    % hold on;
    % visboundaries(edges, 'Color','r');
    % title('Edge Detection of Difference')

    % 5. Enimation
    % subplot(1,4,3)
    % set(p, 'Color', 'w');
    % title('Difference Animation')
    % 
    % for k = 1:10
    %     if mod(k,2) == 0
    %         imshow(targetforPlot);
    %     else
    %         imshow(generatorOutforPlot);
    %     end
    %     title('Difference Animation')
    % 
    %     frame = getframe(p);  % 현재 플롯 캡처
    %     img = frame2im(frame); % 이미지를 RGB로 변환
    %     [A, map] = rgb2ind(img, 256); % GIF 인덱스 변환
    % 
    %     if k == 1
    %         imwrite(A, map, filename, 'gif', 'LoopCount', Inf, 'DelayTime', delayTime);
    %     else
    %         imwrite(A, map, filename, 'gif', 'WriteMode', 'append', 'DelayTime', delayTime);
    %     end
    % end
    % 
    % disp('GIF saved as difference_animation.gif');

    outputFolder = sprintf('C:\\Users\\0043k\\OneDrive\\바탕 화면\\0204_PVForecast\\PredictResults\\predict%dh', predictNum);
    if ~exist(outputFolder)
        mkdir(outputFolder);
    end
    saveas(p, fullfile(outputFolder, sprintf('Predict %d hour Image_%d.png', predictNum, i)));
    i = i + 1;
    close(p);
    
    % 그리고 예측 정확도 수치값 엑셀에 저장하기
    mseV = mean((targetforPlot - generatorOutforPlot).^2, 'all');

    sum((targetforPlot - generatorOutforPlot).^2, 'all')
    % mseV = mean(mse(targetforPlot, generatorOutforPlot));
    mseVals = [mseVals; mseV];

    ssimV = ssim(targetforPlot, generatorOutforPlot);
    ssimVals = [ssimVals; ssimV];

    % optical flow
    if size(targetforPlot, 3) == 3
        targetforPlot_gray = rgb2gray(targetforPlot);
    else
        targetforPlot_gray = targetforPlot;
    end
    if size(generatorOutforPlot, 3) == 3
        generatorOutforPlot_gray = rgb2gray(generatorOutforPlot);
    else
        generatorOutforPlot_gray = generatorOutforPlot;
    end

    opticFlow = opticalFlowFarneback;
    flow1 = estimateFlow(opticFlow, targetforPlot_gray)
    flow2 = estimateFlow(opticFlow, generatorOutforPlot_gray);
    of_mag = sqrt(flow2.Vx.^2 + flow2.Vy.^2);
    of_mag_mean = mean(of_mag, 'all');
    ofVals = [ofVals; of_mag_mean];

    % corr
    corrV = corr2(targetforPlot(:), generatorOutforPlot(:));
    corrVals = [corrVals; corrV];

end

T = table(mseVals, ssimVals, ofVals, corrVals, ...
    'VariableNames', {'MSE', 'SSIM', 'OF', 'Pearson Correlation'});
writetable(T, sprintf('model(predict-%dh)_Results.xlsx', predictNum));
fprintf("엑셀 파일 저장 완.\n");



%% 2) 같은 이미지 예측 시, 모델들 성능 비교
% prepare dataset and networks
folder = 'D:\PV_forecast_2025\천리안2호_적외(구름상)_2021_10min_crop';
imds = imageDatastore(folder, "IncludeSubfolders",true);
inputSize = [128, 128, 3];
imds = augmentedImageDatastore(inputSize(1:2), imds);

load('dlnetGenerator_ir(inputSize128, latentvector256, dongAsia, Epoch50).mat', 'dlnetGenerator');
load('dlnetLSTM_128ir(latentvector256)_PredictTime1h.mat', 'dlnetLSTM'); dlnetLSTM1 = dlnetLSTM;
load('dlnetLSTM_128ir(latentvector256)_PredictTime2h.mat', 'dlnetLSTM'); dlnetLSTM2 = dlnetLSTM;
load('dlnetLSTM_128ir(latentvector256)_PredictTime3h.mat', 'dlnetLSTM'); dlnetLSTM3 = dlnetLSTM;
clear dlnetLSTM;

numInputFrames = 18; % 3시간
MaxTargetFrame = 24;

% Max Frame으로 queue 나누기
numFrame = numInputFrames + MaxTargetFrame;
imds.MiniBatchSize = numFrame;

mbq = minibatchqueue(imds, ...
    'MiniBatchSize', numFrame, ...
    'PartialMiniBatch','discard', ...
    'OutputAsDlarray',true);

i = 1;

mseVals1 = []; mseVals2 = []; mseVals3 = []; mseVals4 = [];
ssimVals1 = []; ssimVals2 = []; ssimVals3 = []; ssimVals4 = [];
ofVals1 = []; ofVals2 = []; ofVals3 =[]; ofVals4 = [];
corrVals1 = []; corrVals2 = []; corrVals3 = []; corrVals4 = [];
while hasdata(mbq)
    % 각 model의 입력 만들기
    dlX = next(mbq);
    targetData = dlX(:,:,:,end);
    numImgsPerhour = 1;
    % inputData_n = dlX(:,:,:,(end-(n+3)*numImgsPerhour+1):(end-n*numImgsPerhour))
    n=1; inputData_1 = dlX(:,:,:,(end-(n+3)*numImgsPerhour+1):(end-n*numImgsPerhour));
    n=2; inputData_2 = dlX(:,:,:,(end-(n+3)*numImgsPerhour+1):(end-n*numImgsPerhour));
    n=3; inputData_3 = dlX(:,:,:,(end-(n+3)*numImgsPerhour+1):(end-n*numImgsPerhour));
    n=4; inputData_4 = dlX(:,:,:,(end-(n+3)*numImgsPerhour+1):(end-n*numImgsPerhour));
    % inputData4 = dlX(:,:,:,(end-(4+3)*6+1):(end-4*6))
    % inputData5 = dlX(:,:,:,(end-(5+3)*6+1):(end-5*6))
    % inputData6 = dlX(:,:,:,(end-(6+3)*6+1):(end-6*6))
    % inputData7 = dlX(:,:,:,(end-(7+3)*6+1):(end-7*6))
    % inputData8 = dlX(:,:,:,(end-(8+3)*6+1):(end-8*6))
    % inputData9 = dlX(:,:,:,(end-(9+3)*6+1):(end-9*6))
    % inputData10 = dlX(:,:,:,(end-(10+3)*6+1):(end-10*6))
    % inputData11 = dlX(:,:,:,(end-(11+3)*6+1):(end-11*6))
    % inputData12 = dlX(:,:,:,(end-(12+3)*6+1):(end-12*6))

    [lstmOut1, generatorOutforPlot1] = GANLSTMmodelOutput(dlnetLSTM1, dlnetGenerator1, inputData1);
    [lstmOut2, generatorOutforPlot2] = GANLSTMmodelOutput(dlnetLSTM2, dlnetGenerator2, inputData2);
    [lstmOut3, generatorOutforPlot3] = GANLSTMmodelOutput(dlnetLSTM3, dlnetGenerator3, inputData3);
    % [lstmOut4, generatorOutforPlot4] = GANLSTMmodelOutput(dlnetLSTM4, dlnetGenerator4, inputData4);
    % [lstmOut5, generatorOutforPlot5] = GANLSTMmodelOutput(dlnetLSTM5, dlnetGenerator5, inputData5);
    % [lstmOut6, generatorOutforPlot6] = GANLSTMmodelOutput(dlnetLSTM6, dlnetGenerator6, inputData6);

    % Plot 
    targetforPlot = rescale(extractdata(targetData));
    d = figure;
    subplot(2,4,1)
    imshow(targetforPlot)
    title('Original Image')

    subplot(2,4,2)
    imshow(generatorOutforPlot1)
    title('Predict 1h model')

    subplot(2,4,3)
    imshow(generatorOutforPlot2)
    title('Predict 2h model')

    subplot(2,4,4)
    imshow(generatorOutforPlot3)
    title('Predict 3h model')

    subplot(2,4,6)
    scatter(1:256, extractdata(squeeze(lstmOut1)), 'filled');
    xlim([0,256])
    title('Predict 1h model: Latent vector')

    subplot(2,4,7)
    scatter(1:256, extractdata(squeeze(lstmOut2)), 'filled');
    xlim([0,256])
    title('Predict 2h model: Latent vector')

    subplot(2,4,8)
    scatter(1:256, extractdata(squeeze(lstmOut3)), 'filled');
    xlim([0,256])
    title('Predict 3h model: Latent vector')

    set(d, "Position", []);
    outputFolder = ''
    if ~exist(outputFolder)
        mkdir(outputFolder)
    end
    saveas(d, fullfile(outputFolder, sprintf('SameTarget Predict Image_%d',i)));
    i = i + 1;
    close(d);
    
    % express difference between images to values
    mseV1 = mean((targetforPlot - generatorOutforPlot1).^2, 'all'); mseVals1 = [mseVals1 ; mseV1];
    mseV2 = mean((targetforPlot - generatorOutforPlot2).^2, 'all'); mseVals2 = [mseVals2 ; mseV2];
    mseV3 = mean((targetforPlot - generatorOutforPlot3).^2, 'all'); mseVals3 = [mseVals3 ; mseV3];


    ssimV1 = ssim(targetforPlot, generatorOutforPlot1); ssimVals1 = [ssimVals1; ssimV1];
    ssimV2 = ssim(targetforPlot, generatorOutforPlot2); ssimVals2 = [ssimVals2; ssimV2];
    ssimV3 = ssim(targetforPlot, generatorOutforPlot3); ssimVals3 = [ssimVals3; ssimV3];
    
    % optical flow
    targetforPlot_gray = rgb2gray(targetforPlot);
    generatorOutforPlot1_gray = rgb2gray(generatorOutforPlot1);
    generatorOutforPlot2_gray = rgb2gray(generatorOutforPlot2);
    generatorOutforPlot3_gray = rgb2gray(generatorOutforPlot3);

    opticFlow = opticalFlowFarneback;
    flow1 = estimateFlow(opticFlow, targetforPlot_gray);
    flow1_1 = estimateFlow(opticFlow, generatorOutforPlot1_gray);
    of_mag1 = sqrt(flow1_1.Vx.^2 + flow1_1.Vx.^2);
    of_mag_mean1 = mean(of_mag1, 'all');
    ofVals1 = [ofVals1; of_mag_mean1];
    
    flow2 = estimateFlow(opticFlow, targetforPlot_gray);
    flow2_1 = estimateFlow(opticFlow, generatorOutforPlot2_gray);
    of_mag2 = sqrt(flow2_1.Vx.^2 + flow2_1.Vx.^2);
    of_mag_mean2 = mean(of_mag2, 'all');
    ofVals2 = [ofVals2; of_mag_mean2];

    flow3 = estimateFlow(opticFlow, targetforPlot_gray);
    flow3_1 = estimateFlow(opticFlow, generatorOutforPlot3_gray);
    of_mag3 = sqrt(flow3_1.Vx.^2 + flow3_1.Vx.^2);
    of_mag_mean3 = mean(of_mag3, 'all');
    ofVals3 = [ofVals3; of_mag_mean3];

    corrV1 = corr2(targetforPlot(:), generatorOutforPlot1(:)); corrVals1 = [corrVals1; corrV1];
    corrV2 = corr2(targetforPlot(:), generatorOutforPlot2(:)); corrVals2 = [corrVals2; corrV2];
    corrV3 = corr2(targetforPlot(:), generatorOutforPlot3(:)); corrVals3 = [corrVals3; corrV3];

end

T_mse = table(mseVals1, mseVals2, mseVals3, ...
    'VariableNames', {'Predict 1h model', 'Predict 2h model' ,'Predict 3h model'});
writetable(T, 'MSE_Results.xlsx');
fprintf("MSE 저장 완.\n");

T_ssim = table(ssimVals1, ssimVals2, ssimVals3, ...
    'VariableNames', {'Predict 1h model', 'Predict 2h model' ,'Predict 3h model'});
writetable(T, 'SSIM_Results.xlsx');
fprintf("SSIM 저장 완.\n");


of_mse = table(ofVals1, ofVals2, ofVals3, ...
    'VariableNames', {'Predict 1h model', 'Predict 2h model' ,'Predict 3h model'});
writetable(T, 'OF_Results.xlsx');
fprintf("OF 저장 완.\n");

corr_mse = table(corrVals1, corrVals2, corrVals3, ...
    'VariableNames', {'Predict 1h model', 'Predict 2h model' ,'Predict 3h model'});
writetable(T, 'corr_Results.xlsx');
fprintf("corr 저장 완.\n");


function [lstmOut, generatorOutforPlot] =  GANLSTMmodelOutput(dlnetLSTM, dlnetGenerator, inputData)
    inputData = dlarray(inputData, 'SSCTB');

    lstmOut = predict(dlnetLSTM, inputData);
    lstmOut = dlarray(lstmOut, 'CBSS');

    generatorOut = predict(dlnetGenerator, lstmOut);
    generatorOut = rescale(generatorOut);
    generatorOutforPlot = rescale(extractdata(generatorOut));
end

