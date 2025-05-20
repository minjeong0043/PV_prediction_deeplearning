clc; clear all; close all;
dataPath = '\\Ugrid\sml_nas\연구용데이터\태풍이미지\3.힌남노';
imds = imageDatastore(dataPath, 'IncludeSubfolders',true);
n = length(imds.Files);
trainIndices = 1:floor(n*0.7); testIndices = trainIndices(end) + 1: trainIndices(end) + floor(n*0.1); validationIndices = testIndices(end)+1:testIndices(end) + floor(n*0.2);
validationimds = subset(imds, validationIndices);
inputSize = [128, 128, 3];
validationimds = augmentedImageDatastore(inputSize(1:2), validationimds);

numInputFrames = 18; numTargetFrame = 6;
[valInput, valTarget] = generateValidationSequence(validationimds, numInputFrames, numTargetFrame)

[valInput2, valTarget2] = generateValidationSequence_v2(validationimds, numInputFrames, numTargetFrame)

isequal(size(valInput), size(valInput2))
isequal(size(valTarget), size(valTarget2))

inputEqual = isequal(extractdata(valInput), extractdata(valInput2))
targetEqual = isequal(extractdata(valTarget), extractdata(valTarget2))

%% Original code
function [data, target] = generateValidationSequence(ds, numframes, targetframe)
celldata = readall(ds); % celldata의 size는 ? ==> 아랫줄 remain이 어떻게 나오는지 확인해보기
remain = mod(size(celldata,1),numframes+targetframe); %4시간 예측 시 numframes 18, targetframe 24
indices = [1:numframes+targetframe:size(celldata,1)-remain-numframes+targetframe];
k = 0;
for i = indices
k = k+1;
% for j = 1:numframes+1
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

%% 수정된 generateValidationSequence
function [data, target] = generateValidationSequence_v2(ds, numframes, targetframe)
celldata = readall(ds); 
remain = mod(size(celldata, 1), numframes + targetframe); 
indices = [1:numframes+targetframe:size(celldata,1)-remain]; 
k = 0;

for i = indices
k = k + 1;
for j = 1:numframes+targetframe
if i + j - 1 <= size(celldata, 1) % 경계 조건 추가
data(:,:,:,j,k) = celldata.input{i+j-1,1};
else
disp("Index out of bounds: "), disp(i + j - 1); % 디버깅용 출력
break;
end
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