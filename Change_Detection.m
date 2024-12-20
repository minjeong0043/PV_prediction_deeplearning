clc; clear all;

dataFolder = 'D:\mj Kim\위성이미지_적외8.7\구름강조(9-11월, 10분단위)_crop';
dataFolder_ir = 'D:\mj Kim\위성이미지_적외8.7\적외선_8.7(9-11월, 10분단위)_crop';

imds = imageDatastore(dataFolder,"IncludeSubfolders",true);
imds_ir = imageDatastore(dataFolder_ir, "IncludeSubfolders",true);

n = length(imds.Files);
n_ir = length(imds_ir.Files);

min_intervals = [10 20 30 40 50 60 70 80 90 100 110 120 180 240 300 360];
mse_results = cell(1, length(min_intervals));
psnr_results = cell(1, length(min_intervals));
ssim_results = cell(1, length(min_intervals));
of_results = cell(1, length(min_intervals));


gpuDevice()
% dataFolder 에 대해서..
for k = 1:length(min_intervals)
    interval = min_intervals(k);
    mse_vals = [];
    psnr_vals = [];
    ssim_vals = [];
    of_vals = [];

    for i = 1:n-interval/10
        % img1 = imread(imds.Files{i});
        % img2 = imread(imds.Files{i+interval/10});
        img1 = gpuArray(imread(imds.Files{i}));
        img2 = gpuArray(imread(imds.Files{i+interval/10}))
        
        mse_v = mean((img1-img2).^2, 'all');
        mse_vals = [mse_vals, gather(mse_v)];

        psnr_v = psnr(img1, img2);
        psnr_vals = [psnr_vals, gather(psnr_v)];

        ssim_v = ssim(img1, img2);
        ssim_vals = [ssim_vals, gather(ssim_v)];

        if size(img1, 3) == 3
            img1_gray = rgb2gray(img1);
        else
            img1_gray = img1;
        end
        if size(img2, 3) == 3
            img2_gray = rgb2gray(img2);
        else
            img2_gray = img2;
        end

        opticFlow = opticalFlowFarneback;
        % flow1 = estimateFlow(opticFlow, img1_gray);
        % flow2 = estimateFlow(opticFlow, img2_gray);
        flow1_gpu = estimateFlow(opticFlow, gather(img1_gray));
        flow2_gpu = estimateFlow(opticFlow, gather(img2_gray));

        magnitude_gpu = sqrt(flow2_gpu.Vx.^2 + flow2_gpu.Vy.^2);
        magnitude_gpu(magnitude_gpu < 1) = 0;
        mag_mean_gpu = mean(magnitude_gpu, 'all');
        of_vals = [of_vals, mag_mean_gpu];

        fprintf('Processing interval %d (%s): %d/%d \n', interval, 'current step', i, n - interval / 10);
    end
    mse_results{k} = mse_vals;
    psnr_results{k} = psnr_vals;
    ssim_results{k} = ssim_vals;
    of_results{k} = of_vals;
end


% 결과 출력
for j = 1:length(time_intervals)
    interval = min_intervals(j);
    
    mse_values = mse_results{j};
    mse_mean = mean(mse_values);
    mse_std = std(mse_values);
    
    psnr_values = psnr_results{j};
    psnr_mean = mean(psnr_values);
    psnr_std = std(psnr_values);
    
    ssim_values = ssim_results{j};
    ssim_mean = mean(ssim_values);
    ssim_std = std(ssim_values);

    of_values = of_results{j};
    of_mean = mean(of_values);
    of_std = std(of_values);

    fprintf('%d분 단위 비교:\n', interval);
    fprintf('MSE 평균: %.2f\n', mse_mean);
    fprintf('MSE 표준편차: %.2f\n', mse_std);
    
    fprintf('PSNR 평균: %.2f\n', psnr_mean);
    fprintf('PSNR 표준편차: %.2f\n', psnr_std);

    fprintf('SSIM 평균: %.4f\n', ssim_mean); % SSIM은 일반적으로 소수점 네 자리로 표시
    fprintf('SSIM 표준편차: %.4f\n\n', ssim_std);

    fprintf('OF 평균: %.4f\n', of_mean); 
    fprintf('OF 표준편차: %.4f\n\n', of_std);
end


% Excel
intervals_column = [];
mse_column = [];
psnr_column = [];
ssim_column = [];
of_column = [];
for j = 1:length(min_intervals)
    interval = min_intervals(j);
    mse_values = mse_results{j};
    psnr_values = psnr_results{j};
    ssim_values = ssim_results{j};
    of_values = of_results{j};
    
    intervals_column = [intervals_column; repmat(interval, length(mse_values), 1)];
    mse_column = [mse_column; mse_values(:)];
    psnr_column = [psnr_column; psnr_values(:)];
    ssim_column = [ssim_column; ssim_values(:)];
    of_column = [of_column; of_values(:)];
end
T = table(intervals_column, mse_column, psnr_column, ssim_column, of_column, ...
          'VariableNames', {'Interval', 'MSE', 'PSNR', 'SSIM', 'OF'});
writetable(T, 'Change Detection results.xlsx');

fprintf('결과 파일 저장완료^^\n');

%% gpu 2개 일 때
clc; clear all;

dataFolder = 'D:\mj Kim\위성이미지_적외8.7\구름강조(9-11월, 10분단위)_crop';
dataFolder_ir = 'D:\mj Kim\위성이미지_적외8.7\적외선_8.7(9-11월, 10분단위)_crop';

imds = imageDatastore(dataFolder, "IncludeSubfolders", true);
imds_ir = imageDatastore(dataFolder_ir, "IncludeSubfolders", true);

n = length(imds.Files);
n_ir = length(imds_ir.Files);

min_intervals = [10 20 30 40 50 60 70 80 90 100 110 120 180 240 300 360];
mse_results = cell(1, length(min_intervals));
psnr_results = cell(1, length(min_intervals));
ssim_results = cell(1, length(min_intervals));
of_results = cell(1, length(min_intervals));

availableGPUs = gpuDeviceCount("available");
if availableGPUs < 2
    error('This code requires at least two GPUs.');
end

parpool("Processes", availableGPUs);

parfor k = 1:length(min_intervals)
    interval = min_intervals(k);
    mse_vals = [];
    psnr_vals = [];
    ssim_vals = [];
    of_vals = [];

    gpuIndex = mod(k - 1, availableGPUs) + 1; 
    gpuDevice(gpuIndex);

    for i = 1:n - interval / 10

        img1 = gpuArray(imread(imds.Files{i}));
        img2 = gpuArray(imread(imds.Files{i + interval / 10}));

        mse_v = mean((img1 - img2).^2, 'all');
        mse_vals = [mse_vals, gather(mse_v)]; % CPU로 결과 전송

        psnr_v = psnr(img1, img2);
        psnr_vals = [psnr_vals, gather(psnr_v)];

        ssim_v = ssim(img1, img2);
        ssim_vals = [ssim_vals, gather(ssim_v)];

        if size(img1, 3) == 3
            img1_gray = rgb2gray(img1);
        else
            img1_gray = img1;
        end

        if size(img2, 3) == 3
            img2_gray = rgb2gray(img2);
        else
            img2_gray = img2;
        end

        opticFlow = opticalFlowFarneback;
        flow1_gpu = estimateFlow(opticFlow, gather(img1_gray)); % GPU -> CPU 변환 필요
        flow2_gpu = estimateFlow(opticFlow, gather(img2_gray));

        magnitude_gpu = sqrt(flow2_gpu.Vx.^2 + flow2_gpu.Vy.^2);
        magnitude_gpu(magnitude_gpu < 1) = 0;

        mag_mean_gpu = mean(magnitude_gpu, 'all');
        of_vals = [of_vals, mag_mean_gpu];

        fprintf('Processing interval %d (%s): %d/%d \n', interval, 'current step', i, n - interval / 10);
    end

    mse_results{k} = mse_vals;
    psnr_results{k} = psnr_vals;
    ssim_results{k} = ssim_vals;
    of_results{k} = of_vals;
end

delete(gcp('nocreate'));
