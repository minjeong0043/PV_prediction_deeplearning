clc; clear all;
folder = 'C:\Users\leejunwoo\OneDrive - 고려대학교\juan\바탕 화면_준현\mj Kim\위성이미지_적외8.7\245031\work\01';
files = dir(fullfile(folder, '*.png'));
files = natsortfiles({files.name});

n = length(files);
images = cell(1, n);
for i = 1:n
    img = imread(fullfile(folder, files{i}));
    images{i} = img;
end

time_intervals = [10 20 30 40 50 60 70 80 90 100 110];
mse_results = cell(1, length(time_intervals));
psnr_resuls = cell(1, length(time_intervals));
ssim_results = cell(1, length(time_intervals));
for k = 1:length(time_intervals)
    interval = time_intervals(k);
    mse_values = [];
    psnr_values = [];
    ssim_values = [];
    for i = 1:n-interval/10
        img1 = images{i};
        img2 = images{i+interval/10};

        mse = mean((img1-img2).^2, 'all');
        mse_values = [mse_values, mse];

        psnr_value = psnr(img1, img2);
        psnr_values = [psnr_values, psnr_value];

        ssim_value = ssim(img1, img2);
        ssim_values = [ssim_values, ssim_value];
    end
    mse_results{k} = mse_values
    psnr_results{k} = psnr_values
    ssim_results{k} = ssim_values
end

% 결과 출력
for j = 1:length(time_intervals)
    interval = time_intervals(j);
    
    mse_values = mse_results{j};
    mse_mean = mean(mse_values);
    mse_std = std(mse_values);
    
    psnr_values = psnr_results{j};
    psnr_mean = mean(psnr_values);
    psnr_std = std(psnr_values);
    
    ssim_values = ssim_results{j};
    ssim_mean = mean(ssim_values);
    ssim_std = std(ssim_values);

    fprintf('%d분 단위 비교:\n', interval);
    fprintf('MSE 평균: %.2f\n', mse_mean);
    fprintf('MSE 표준편차: %.2f\n', mse_std);
    
    fprintf('PSNR 평균: %.2f\n', psnr_mean);
    fprintf('PSNR 표준편차: %.2f\n', psnr_std);

    fprintf('SSIM 평균: %.4f\n', ssim_mean); % SSIM은 일반적으로 소수점 네 자리로 표시
    fprintf('SSIM 표준편차: %.4f\n\n', ssim_std);
end



% Excel
intervals_column = [];
mse_column = [];
psnr_column = [];
ssim_column = [];
for j = 1:length(time_intervals)
    interval = time_intervals(j);
    mse_values = mse_results{j};
    psnr_values = psnr_results{j};
    ssim_values = ssim_results{j};
    
    intervals_column = [intervals_column; repmat(interval, length(mse_values), 1)];
    mse_column = [mse_column; mse_values(:)];
    psnr_column = [psnr_column; psnr_values(:)];
    ssim_column = [ssim_column; ssim_values(:)];
end
T = table(intervals_column, mse_column, psnr_column, ssim_column, ...
          'VariableNames', {'Interval', 'MSE', 'PSNR', 'SSIM'});
writetable(T, 'image_quality_metrics.xlsx');

fprintf('MSE, PSNR 및 SSIM 결과가 Excel 파일 저장완료^^\n');