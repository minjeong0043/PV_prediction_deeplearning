clc; clear all; close all;

gpuInfo = gpuDevice();
fprintf("Available GPU memory: %.2f GB\n", gpuInfo.AvailableMemory / 1e9);
% prepare dataset
folder = 'C:\Users\minjeong\Desktop\PV_forecast_2024\적외선_8.7(9-11월, 10분단위)_crop';
imds = imageDatastore(folder, "IncludeSubfolders",true);

n = length(imds.Files);
 
trainIndices = 1:floor(n*0.7);
testIndices = trainIndices(end) + 1: trainIndices(end)+ floor(n*0.1);
validationIndices = testIndices(end) + 1:testIndices(end) + floor(n*0.2);

trainimds = subset(imds, trainIndices);
testimds = subset(imds, testIndices);
validationimds = subset(imds, validationIndices);

inputSize = [128, 128, 3];
% inputSize = [256, 256, 3];
% inputSize = [512, 512, 3];

trainimds = augmentedImageDatastore(inputSize(1:2), trainimds);
testimds = augmentedImageDatastore(inputSize(1:2), testimds);
validationimds = augmentedImageDatastore(inputSize(1:2), validationimds);

% set param
numInputFrames = 18; % 3hours
numTargetFrame = 6; % 1hour
% numTargetFrame = 12; %2hour
% numTargetFrame = 18; %3hour

trainImdsSequence = trainimds;

trainImdsSequence.MiniBatchSize = numInputFrames + numTargetFrame; 



% Define layer
% numFilters = 64;
numFilters = 256;
dlnetLSTM = [
    sequenceInputLayer(inputSize,"Normalization",'none',"Name","inputlstm")
    convolution2dLayer(3,32,'Padding','same','Name','conv1lstm','Stride',2,'WeightsInitializer','he')
    reluLayer('Name','relu1lstm')
    convolution2dLayer(3,64,'Padding','same','Name','conv2lstm','Stride',2,'WeightsInitializer','he')
    reluLayer('Name','relu2lstm')
    convolution2dLayer(3,128,'Padding','same','Name','conv3lstm','Stride',2,'WeightsInitializer','he')
    reluLayer('Name','relu3lstm')
    dropoutLayer(0.5,'Name','dropout')
    lstmLayer(numFilters,'OutputMode','last','Name','lstm2','InputWeightsInitializer', 'narrow-normal','RecurrentWeightsInitializer','narrow-normal') % lstm num hidden units should match the numfilters of the generator.
    ];
dlnetLSTM = dlnetwork(dlnetLSTM);

load("dlnetGenerator_128ir(Epoch300,latentvector256).mat", 'dlnetGenerator');
disp("Before training")

% training 
start = tic;
learnRate = 0.0002;
squaredGradientsAvg = [];
numEpochsLSTM = 100;
validationFrequency = 5;

[valInput, valTarget] = generateValidationSequence(validationimds, numInputFrames, numTargetFrame);
% Adam param
beta1 = 0.9;
beta2 = 0.999;
epsilon = 1e-8;
moment1 = [];
moment2 = [];
timeStep = 0;

iteration = 0;
figure;

for epoch = 1:numEpochsLSTM
    reset(trainImdsSequence); 
    while hasdata(trainImdsSequence)
        iteration = iteration + 1;

        data = read(trainImdsSequence); 

        if size(data, 1) == numInputFrames + numTargetFrame
            [inputData, targetData] = processSequence(data, numTargetFrame);
            [gradientsModel, loss] = dlfeval(@modelGradients, inputData, targetData, dlnetGenerator, dlnetLSTM);
            % [dlnetLSTM, squaredGradientsAvg] = rmspropupdate(dlnetLSTM, gradientsModel, squaredGradientsAvg, learnRate);
            timeStep = timeStep + 1;
            [dlnetLSTM, moment1, moment2] = adamupdate(dlnetLSTM, gradientsModel, moment1, moment2, timeStep, learnRate, beta1, beta2, epsilon);
            
            D = duration(0,0,toc(start), 'Format', 'hh:mm:ss');
                       
            fprintf("Epoch : %d, Iteration : %d, Training Loss : %f\n",epoch, iteration, loss);
        end
    end
    
    if mod(epoch, validationFrequency) == 0
        valout = predictLSTMGAN(dlnetLSTM, dlnetGenerator, valInput);
        valloss = mse(valout, valTarget);

        fprintf("Validation loss : %f\n", valloss);
        valout = [valout, valTarget];
        valout = gather(extractdata(valout));
        montage(valout);
        title(sprintf('Epoch %d - Validation Results', epoch));
        outputFolder = 'C:\Users\minjeong\Desktop\PV_forecast_2024\code\250123)grayimg_LSTM\output';
        saveas(h, fullfile(outputFolder, sprintf('Epoch%d_ValidationResult.png', epoch)));
        close(h)
    end
end




save('dlnetLSTM_128ir(latentvector256)', "dlnetLSTM")


function [gradients, loss] = modelGradients(X,Y,generator,lstm)
% Forward input through LSTM + GAN network.
predicted = forwardLSTMGAN(lstm, generator, X);

% Compute the mse loss.
loss = mse(predicted,Y);

% Compute the gradients only w.r.t to the lstm model, We don't want to
% train the generator weights.
gradients = dlgradient(loss,lstm.Learnables);
end

function [data, target] = processSequence(tableData, targetframe)
% Create the sequence for input.
for i = 1:size(tableData,1)
    data(:,:,:,i) = tableData.input{i,1};
end

% Normalize data in the range 0-1.
data = im2single(data);
target = data(:,:,:,end);
data = data(:,:,:,1:end-targetframe);

% Add dataformat label "SSCTB".
data = dlarray(data,"SSCTB");
target = dlarray(target,"SSCB");

% Move to gpu.
if canUseGPU
    data = gpuArray(data);
end
end

function generatorOut = forwardLSTMGAN(lstmNet, generatorNet, input)
% Get output from LSTM.
lstmOut = forward(lstmNet, input);
% Convert output of lstm to CBSS for generator.
lstmOut = dlarray(lstmOut,"CBSS");
% Get output from generator.
generatorOut = predict(generatorNet,lstmOut);
% Rescale the generator output to 0-1 range.
generatorOut = rescale(generatorOut);
end

function generatorOut = predictLSTMGAN(lstmNet, generatorNet, input)
% Get output from LSTM.
lstmOut = predict(lstmNet, input);
% Convert output of lstm to CBSS for generator.
lstmOut = dlarray(lstmOut,"CBSS");
% Get output from generator.
generatorOut = predict(generatorNet,lstmOut);
% Rescale the generator output to 0-1 range.
generatorOut = rescale(generatorOut);
end

function [data, target] = generateValidationSequence(ds, numframes, targetframe)
celldata = readall(ds);
remain = mod(size(celldata,1),numframes+targetframe);
indices = [1:numframes+targetframe:size(celldata,1)-remain-numframes+targetframe];
k = 0;
for i = indices
    k = k+1;
%     for j = 1:numframes+1
    for j = 1:numframes+targetframe
        data(:,:,:,j,k) = celldata.input{i+j-1,1};
    end
end

% Normalize data in the range 0-1.
data = im2single(data);
target = squeeze(data(:,:,:,end,:));
data = data(:,:,:,1:end-targetframe,:);

% Add dataformat label "SSCTB".
data = dlarray(data,"SSCTB");
target = dlarray(target,"SSCB");

% Move to gpu.
if canUseGPU
    data = gpuArray(data);
end
end