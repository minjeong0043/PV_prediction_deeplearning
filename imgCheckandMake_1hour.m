clc; clear all; close all;

folder = 'C:\Users\minjeong\Desktop\천리안2호_적외(구름상)_2020~2022_1hour_crop';
files = dir(fullfile(folder, '*.png'));
files = natsortfiles({files.name});
n = length(files)
%% 만든 이미지 지우기
n = length(files);
for i = 1:n
    if length(files{i}) ~= 44
        delete(fullfile(folder, files{i}))
        fprintf('delete file : %s\n', files{i});
    end
end
fprintf("total files  %d\n", n)

%% 이미지 누락 파일 확인
clc; clear all; close all;

folder = 'C:\Users\minjeong\Desktop\천리안2호_적외(구름상)_2020~2022_1hour_crop';
files = dir(fullfile(folder, '*.png'));
files = natsortfiles({files.name});
n = length(files)

hour_index = ["15", "16", "17", "18", "19", "20", "21", "22", "23", ...
              "00", "01", "02", "03", "04", "05", "06", "07", "08", ...
              "09", "10", "11", "12", "13", "14"];
hour_bias = find(hour_index == '06')
index_h = hour_bias;

for i = 1:n
    hour = string(files{i}(37:38));
    expected_hour = hour_index(index_h);
    fprintf("current file : %s, expected hour : %s\n", files{i}, expected_hour);
    if hour ~= expected_hour
        fprintf('Missing File before: %s\n', files{i});
        index_h = index_h + 1;
        if index_h> length(hour_index)
            index_h = 1;
        end

        % 대체 파일 생성
        oldFilePath = fullfile(folder, files{i-1});
        file_hIndex = find(hour_index == oldFilePath(98:99));
        file_hIndex_new = file_hIndex+1;
        if file_hIndex_new > length(hour_index)
            file_hIndex_new = 1;
        end
        newFilesPath = string(oldFilePath(1:97)) + hour_index(file_hIndex_new) + "00_" + hour_index(file_hIndex) + "00"+".png";
        copyfile(oldFilePath, newFilesPath);
        if exist(newFilesPath)
            fprintf('~~~~~~~Making file : %s\n', newFilesPath);
        end
        pause(1)
        % break
        % index_h = index_h + 1;
    end

    index_h = index_h + 1;
    if index_h > length(hour_index)
        index_h = 1;
    end
end

fprintf('Complete checking\n')

