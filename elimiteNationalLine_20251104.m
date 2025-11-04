clc; clear all;

folder = "K:\적외선_8.7(2021~2023년, 10분단위)_crop";
saveFolder = 'D:\천리안2호_적외8.7(2021-2022, 10분단위)_crop';
% List all image files in the specified folder
imageFiles = dir(fullfile(folder, '*.png'));
imageFiles = {imageFiles.name}';
start = tic;
parfor i = 1: length(imageFiles)/3*2
    img_path = fullfile(folder, imageFiles{i});
    save_path = fullfile(saveFolder, imageFiles{i});
    EliminateNationalLine(img_path, save_path);
    D = duration(0,0,toc(start),'Format','hh:mm:ss');
    fprintf('(%d / %d) image name : %s, Elapsed : %s\n', i, length(imageFiles)/3*2, imageFiles{i}, string(D))
end

%% one file
function EliminateNationalLine(img_path, save_path)
orig_img = imread(img_path);   % 원본 이미지
img = double(orig_img);        % 작업용 이미지

% 원본의 "완전히 검은색 배경" 위치 저장 (모든 채널이 0)
orig_black_mask = all(orig_img == 0, 3);

% 국경선(노란색 계열) 마스크 생성
yellow_mask = img(:,:,1) >= 121 & img(:,:,2) >= 121 & img(:,:,3) <= 120;

% 국경선 부분만 검은색(0,0,0)으로 변경
img(repmat(yellow_mask, [1, 1, 3])) = 0;

repeatCount = 2;
filterSize = 5;
halfSize = floor(filterSize/2);

for rep = 1:repeatCount
    for c = 1:3
        channel = img(:,:,c);
        filledChannel = channel; % 결과 저장용

        for y = 1:size(channel,1)
            for x = 1:size(channel,2)
                % **원래 검은색이 아니고 & 스무딩용 검은색**만 처리
                if ~orig_black_mask(y,x) && yellow_mask(y,x) && channel(y,x)==0
                    y1 = max(1, y-halfSize);
                    y2 = min(size(channel,1), y+halfSize);
                    x1 = max(1, x-halfSize);
                    x2 = min(size(channel,2), x+halfSize);

                    window = channel(y1:y2, x1:x2);

                    % 주변에서 검은색(스무딩 마스크)과 중심 제외
                    window_mask = ~( (window==0) | ((y1:y2)'==y & (x1:x2)==x) );
                    numValid = nnz(window_mask);

                    if numValid > 0
                        neighborAvg = mean(window(window_mask));
                        filledChannel(y,x) = neighborAvg;
                    else
                        filledChannel(y,x) = 0;
                    end
                end
            end
        end
        img(:,:,c) = filledChannel;
    end
end

img = uint8(img);
imwrite(img, save_path)

end
