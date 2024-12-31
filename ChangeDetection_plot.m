% Change Detection plot
clc; clear all;

data = readtable("Change Detection results(구름강조_9to11)_241228.xlsx");

intervals = data.Interval;
mse_data = data.MSE;
psnr_data = data.PSNR;
ssim_data = data.SSIM;
of_data = data.OF;



% avg plot
interval_u = unique(intervals)
mse_avg = zeros(numel(interval_u), 1)
psnr_avg = zeros(numel(interval_u), 1)
ssim_avg = zeros(numel(interval_u), 1)
of_avg = zeros(numel(interval_u), 1)

for i = 1:numel(interval_u)
    indices = find(intervals == interval_u(i));
    mse_avg(i) = mean(mse_data(indices));
    psnr_avg(i) = mean(psnr_data(indices));
    ssim_avg(i) = mean(ssim_data(indices));
    of_avg(i) = mean(of_data(indices));
end

figure;
subplot(4,2,1)
boxchart(intervals, mse_data, 'BoxWidth', 5);
xlabel('Intervals [min]')
ylabel('MSE')
xticks(unique(intervals));

subplot(4,2,2)
scatter(interval_u, mse_avg)
xlabel('Intervals [min]')
ylabel('Average of MSE')
xticks(unique(intervals));

subplot(4,2,3);
boxchart(intervals, psnr_data, 'BoxWidth', 5);
xlabel('Intervals [min]')
ylabel('PSNR')
xticks(unique(intervals));

subplot(4,2,4)
scatter(interval_u, psnr_avg)
xlabel('Intervals [min]')
ylabel('Average of PSNR')
xticks(unique(intervals));

subplot(4,2,5)
boxchart(intervals, ssim_data, 'BoxWidth', 5);
xlabel("Intervals [min]")
ylabel('SSIM')
xticks(unique(intervals))

subplot(4,2,6)
scatter(interval_u, ssim_avg)
xlabel('Intervals [min]')
ylabel('Average of SSIM')
xticks(unique(intervals));

subplot(4,2,7)
boxchart(intervals, of_data, 'BoxWidth', 5);
xlabel("Intervals [min]")
ylabel("OF")
xticks(unique(intervals))

subplot(4,2,8)
scatter(interval_u, of_avg)
xlabel('Intervals [min]')
ylabel('Average of OF')
xticks(unique(intervals));

