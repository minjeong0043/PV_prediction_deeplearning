clc;clear all; close all;

data1h = readtable("model(predict-1h)_Results_6000.xlsx");
data2h = readtable("model(predict-2h)_Results_6000.xlsx");

mse1 = data1h.MSE
mse2 = data2h.MSE

ssim1 = data1h.SSIM
ssim2 = data2h.SSIM

of1 = data1h.OF
of2 = data2h.OF

corr1 = data1h.PearsonCorrelation
corr2 = data2h.PearsonCorrelation


% MSE
mu1 = mean(mse1); sigma1 = std(mse1);
mu2 = mean(mse2); sigma2 = std(mse2);

%%
clc; clear all; close all;

% 데이터 읽기
data1h = readtable("model(predict-1h)_Results_6000.xlsx");
data2h = readtable("model(predict-2h)_Results_6000.xlsx");

% MSE 값 추출m
mse1 = data1h.PearsonCorrelation;
mse2 = data2h.PearsonCorrelation;

% 데이터 결합 및 그룹화
all_data = [mse1; mse2];
group = [repmat("1시간 예측", length(mse1), 1); repmat("2시간 예측", length(mse2), 1)];

% 그룹 데이터를 범주형으로 변환
group = categorical(group);

% 박스 차트 생성
figure;
boxchart(group, all_data);

% 그래프 제목 및 축 레이블 설정
title('PearsonCorrelation 분포');
xlabel('예측 시간');
ylabel('PearsonCorrelation 값');
grid on;

%%
clc; clear all; close all;

% 데이터 불러오기
data1h = readtable("model(predict-1h)_Results_6000.xlsx");
data2h = readtable("model(predict-2h)_Results_6000.xlsx");

% 'MSE' 열 가져오기
mse1 = data1h.MSE;
mse2 = data2h.MSE;

% 평균과 표준편차 계산
mu1 = mean(mse1);
sigma1 = std(mse1);

mu2 = mean(mse2);
sigma2 = std(mse2);

% X축 레이블 설정
x_labels = categorical({'1h', '2h'}); % 막대 이름

% 막대 그래프 그리기
figure;
bar(x_labels, [mu1, mu2]); 
hold on;

% 표준편차를 에러바(error bar)로 추가
errorbar(x_labels, [mu1, mu2], [sigma1, sigma2], 'k', 'LineStyle', 'none', 'LineWidth', 2);

% 그래프 스타일 설정
ylabel('MSE 평균');
title('1h vs 2h MSE 평균과 표준편차');
grid on;
hold off;


%%

figure;
boxchart(1, mse1)