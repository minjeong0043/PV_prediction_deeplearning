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
