clc; clear all;
% gpuDevice(1)
datasetFolder = 'D:\PV_forecast_2025\천리안2호_적외(구름상)_2019~2023_10min_crop';

imds = imageDatastore(datasetFolder, "IncludeSubfolders",true);

filesIndices = 1:size(imds.Files, 1);
trainIndices = 1:floor(0.7*size(imds.Files, 1));
testIndices = trainIndices(end) + 1: trainIndices(end) + floor(0.2*size(imds.Files, 1));
validationIndices = testIndices(end) + 1: testIndices(end) + floor(0.1*size(imds.Files, 1));

trainimds = subset(imds, trainIndices);
testimds = subset(imds, testIndices);
validationimds = subset(imds, validationIndices);

inputSize = [128, 128, 3];

trainimds = augmentedImageDatastore(inputSize(1:2), trainimds);
testimds = augmentedImageDatastore(inputSize(1:2), testimds);
validationimds = augmentedImageDatastore(inputSize(1:2), validationimds);

% Define layer
filterSize = 5;
numFilters = 64;
numLatentInputs = 256;
projectionSize = [8 8 512];
layerG = [
    imageInputLayer([1 1 numLatentInputs],'Normalization','rescale-symmetric','min',-3,'max',3,'Name','in')
    projectAndReshapeLayer(projectionSize);
    transposedConv2dLayer(filterSize,4*numFilters,'Stride',2,'Cropping','same','Name','tconv1','WeightsInitializer','he')
    batchNormalizationLayer('Name','bnorm1')
    reluLayer('Name','relu1')
    transposedConv2dLayer(filterSize,2*numFilters,'Stride',2,'Cropping','same','Name','tconv2','WeightsInitializer','he')
    batchNormalizationLayer('Name','bnorm2')
    reluLayer('Name','relu2')
    transposedConv2dLayer(filterSize,numFilters,'Stride',2,'Cropping','same','Name','tconv3','WeightsInitializer','he')
    batchNormalizationLayer('Name','bnorm3')
    reluLayer('Name','relu3')
    transposedConv2dLayer(filterSize,inputSize(3),'Stride',2,'Cropping','same','Name','tconv4')
    tanhLayer('Name','tanh')];
dlnetGenerator = dlnetwork(layerG)

dropoutProb = 0.5;
numFilters = 64;
scale = 0.2;
filterSize = 5;
layerD = [
    imageInputLayer(inputSize,'Normalization','rescale-symmetric','Min',-3,'Max',3,'Name','in')
    convolution2dLayer(filterSize,numFilters,'Stride',2,'Padding','same','Name','conv1','WeightsInitializer','he')
    leakyReluLayer(scale,'Name','lrelu1')
    convolution2dLayer(filterSize,2*numFilters,'Stride',2,'Padding','same','Name','conv2','WeightsInitializer','he')
    batchNormalizationLayer('Name','bn2')
    leakyReluLayer(scale,'Name','lrelu2')
    convolution2dLayer(filterSize,4*numFilters,'Stride',2,'Padding','same','Name','conv3','WeightsInitializer','he')
    batchNormalizationLayer('Name','bn3')
    leakyReluLayer(scale,'Name','lrelu3')
    convolution2dLayer(filterSize,8*numFilters,'Stride',2,'Padding','same','Name','conv4','WeightsInitializer','he')
    batchNormalizationLayer('Name','bn4')
    leakyReluLayer(scale,'Name','lrelu4')
    convolution2dLayer(4,1,'Name','conv5')
    dropoutLayer(0.5,'Name','dropout')
    globalAveragePooling2dLayer('Name','avgPooling')];
dlnetDiscriminator = dlnetwork(layerD)

% Train
% numEpochs = 50;
numEpochs = 50;
minibatchSize = 128;
% minibatchSize = 64;
% minibatchSize = 32;
learnRate = 0.0002;
gradientDecayFactor = 0.5;
squaredGradientDecayFactor = 0.999;

fliFactor = 0.3;
validationFrequency = 25;

trainimds.MiniBatchSize = minibatchSize;
executionEnvironment = "auto";
mbq = minibatchqueue(trainimds, ...
    'MiniBatchSize',minibatchSize,...
    'PartialMiniBatch','return',...
    'MiniBatchFcn', @preprocessMiniBatch,...
    'MiniBatchFormat','SSCB',...
    'OutputEnvironment',executionEnvironment);

trailingAvgGenerator = [];
trailingAvgSqGenerator = [];
trailingAvgDiscriminator = [];
trailingAvgSqDiscriminator = [];

numValidationImages = 25;
ZValidation = randn(1,1,numLatentInputs,numValidationImages,'single');
dlZValidation = dlarray(ZValidation,'SSCB');

f = figure;
f.Position(3) = 2*f.Position(3);

imageAxes = subplot(1,2,1);
scoreAxes = subplot(1,2,2);
lineScoreGenerator = animatedline(scoreAxes,'Color',[0 0.447 0.741]);
lineScoreDiscriminator = animatedline(scoreAxes, 'Color', [0.85 0.325 0.098]);
legend('Generator','Discriminator');
ylim([0 1])
xlabel("Iteration")
ylabel("Score")
grid on

iteration = 0;
start = tic;

flipFactor = 0.3;

for epoch = 1:numEpochs
    shuffle(mbq);

    while hasdata(mbq)
        iteration = iteration +  1;
        dlX = next(mbq);

        Z = randn(1,1,numLatentInputs, size(dlX, 4), 'single');
        dlZ = dlarray(Z, 'SSCB');

        if (executionEnvironment == "auto" && canUseGPU) || executionEnvironment == "gpu"
            dlZ = gpuArray(dlZ);
        end
        [gradientsGenerator, gradientsDiscriminator, stateGenerator, scoreGenerator, scoreDiscriminator] = ...
            dlfeval(@modelGradients, dlnetGenerator, dlnetDiscriminator, dlX, dlZ, flipFactor);
        dlnetGenerator.State = stateGenerator;
        [dlnetDiscriminator,trailingAvgDiscriminator,trailingAvgSqDiscriminator] = ...
            adamupdate(dlnetDiscriminator, gradientsDiscriminator, ...
            trailingAvgDiscriminator, trailingAvgSqDiscriminator, iteration, ...
            learnRate, gradientDecayFactor, squaredGradientDecayFactor);

        [dlnetGenerator,trailingAvgGenerator,trailingAvgSqGenerator] = ...
            adamupdate(dlnetGenerator, gradientsGenerator, ...
            trailingAvgGenerator, trailingAvgSqGenerator, iteration, ...
            learnRate, gradientDecayFactor, squaredGradientDecayFactor);

        if mod(iteration,validationFrequency) == 0 || iteration == 1
            dlXGeneratedValidation = predict(dlnetGenerator,dlZValidation);
            
            I = imtile(extractdata(dlXGeneratedValidation));
            I = rescale(I);
            subplot(1,2,1);
            image(imageAxes,I)
            xticklabels([]);
            yticklabels([]);
            title("Generated Images");

        end
        
        % Update the scores plot.
        subplot(1,2,2)
        addpoints(lineScoreGenerator,iteration,...
            double(gather(extractdata(scoreGenerator))));
        
        addpoints(lineScoreDiscriminator,iteration,...
            double(gather(extractdata(scoreDiscriminator))));
        
        D = duration(0,0,toc(start),'Format','hh:mm:ss');
        title(...
            "Epoch: " + epoch + ", " + ...
            "Iteration: " + iteration + ", " + ...
            "Elapsed: " + string(D))
        
        drawnow
    end
end

% % save model
% plot(dlnetGenerator)
save('dlnetGenerator_ir(inputSize128, latentvector256, dongAsia, Epoch50)', 'dlnetGenerator')

function [gradientsGenerator, gradientsDiscriminator, stateGenerator, scoreGenerator, scoreDiscriminator] = ...
    modelGradients(dlnetGenerator, dlnetDiscriminator, dlX, dlZ, flipFactor)

% Calculate the predictions for real data with the discriminator network.
dlYPred = forward(dlnetDiscriminator, dlX);


% Calculate the predictions for generated data with the discriminator network.
[dlXGenerated,stateGenerator] = forward(dlnetGenerator,dlZ);
dlYPredGenerated = forward(dlnetDiscriminator, dlXGenerated);

% Convert the discriminator outputs to probabilities.
probGenerated = sigmoid(dlYPredGenerated);
probReal = sigmoid(dlYPred);

% Calculate the score of the discriminator.
scoreDiscriminator = ((mean(probReal)+mean(1-probGenerated))/2);

% Calculate the score of the generator.
scoreGenerator = mean(probGenerated);

% Randomly flip a fraction of the labels of the real images.
if flipFactor ~= 0
    numObservations = size(probReal,4);
    idx = randperm(numObservations,floor(flipFactor * numObservations));
    
    % Flip the labels.
    probReal(:,:,:,idx) = 1-probReal(:,:,:,idx);
end

% Calculate the GAN loss.
[lossGenerator, lossDiscriminator] = ganLoss(probReal,probGenerated);

% For each network, calculate the gradients with respect to the loss.
gradientsGenerator = dlgradient(lossGenerator, dlnetGenerator.Learnables,'RetainData',true);
gradientsDiscriminator = dlgradient(lossDiscriminator, dlnetDiscriminator.Learnables);

end

function [lossGenerator, lossDiscriminator] = ganLoss(probReal,probGenerated)

% Calculate the loss for the discriminator network.
lossDiscriminator =  -mean(log(probReal)) -mean(log(1-probGenerated));

% Calculate the loss for the generator network.
lossGenerator = -mean(log(probGenerated));

end

function X = preprocessMiniBatch(data)
    % Concatenate mini-batch
    X = cat(4,data{:});
    
    % Rescale the images in the range [-1 1].
    X = rescale(X,-1,1,'InputMin',0,'InputMax',255);
end

% gpuDevice()
