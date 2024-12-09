% 이미지 개수 맞게 저장됐는지, 어느 부분이 빠졌는지 확인하는 코드
clc; clear all;

% 폴더 경로 설정
folder = 'D:\mj Kim\위성이미지_적외8.7\구름강조 11월';
files = dir(fullfile(folder, '*.png')); % 폴더 내 PNG 파일 목록 가져오기
files = natsortfiles({files.name}); % 자연 정렬

% 시간 및 분 단위 배열 정의
hour_index = ["15", "16", "17", "18", "19", "20", "21", "22", "23", ...
              "00", "01", "02", "03", "04", "05", "06", "07", "08", ...
              "09", "10", "11", "12", "13", "14"];
min_index = ["00", "10", "20", "30", "40", "50"]; 

n = length(files); % 파일 개수

% 누락된 파일 확인
h = 1; % 시간 인덱스 초기화
for i = 1:n
    % 파일 이름에서 시간과 분 추출 (파일 이름 구조에 따라 수정 필요)
    hour = string(files{i}(38:39)); % 시간 (문자열로 변환)
    min = string(files{i}(40:41)); % 분 (문자열로 변환)

    % 예상되는 분 단위 계산
    expected_min = min_index(mod(i-1, 6)+1);

    % 시간 비교
    if hour ~= hour_index(h)
        fprintf('HOUR) Missing file before: %s\n', files{i}); 
        break; % 중단 (첫 번째 누락된 파일만 확인)
    else
        % 분 비교
        if expected_min ~= min
            fprintf('MIN) Missing file before: %s\n', files{i});
            break; % 중단 (첫 번째 누락된 파일만 확인)
        end
    end

    % 시간 인덱스 증가 (분이 '50'인 경우 다음 시간으로 이동)
    if expected_min == "50"
        h = h + 1;
        if h > length(hour_index) % 시간 인덱스 초과 방지
            h = 1;
        end
    end
end

fprintf('File check completed.\n');

%% 날짜또한 있는지 확인 
% 8월 31일 ~ 9월 30일까지...
clc; clear all;
folder = 'D:\mj Kim\위성이미지_적외8.7\구름강조 11월';
files = dir(fullfile(folder, '*.png'));
file_name = natsortfiles({files.name})
file_name{1}
file_name{1}(36:37)

n = length(file_name);
day_prev = 30;
for i=1:n
    day = file_name{i}(36:37);
    if day_prev ~=day
        print('day : %d\n', day)
    end
    day
end

%%
clc; clear all;

% Folder path
folder = 'D:\mj Kim\위성이미지_적외8.7\구름강조 11월';
files = dir(fullfile(folder, '*.png')); % List all PNG files
file_names = natsortfiles({files.name}); % Natural sorting of filenames

n = length(file_names);

% Initialize variables
unique_days = {}; % To store unique days
day_counts = [];  % To store counts of data for each day

% Loop through all files to extract days and count occurrences

for i = 1:n
    day = file_names{i}(36:37); % Extract day part (assuming day is at position 36:37)
    
    % Check if the day is already in the unique_days list
    if isempty(unique_days) || ~ismember(day, unique_days)
        unique_days = [unique_days; day]; % Add new unique day
        day_counts = [day_counts; 1];     % Initialize count for this day
    else
        % Increment count for the existing day
        idx = find(strcmp(unique_days, day));
        day_counts(idx) = day_counts(idx) + 1;
    end
end

% Display results
fprintf('Day changes and their data counts:\n');
for i = 1:length(unique_days)
    fprintf('Day: %s, Count: %d\n', unique_days{i}, day_counts(i));
end

fprintf('Total unique days: %d\n', length(unique_days));


%%
clc; clear all;

% Folder path
folder = 'D:\mj Kim\위성이미지_적외8.7\구름강조(9-11월, 10분단위)';
files = dir(fullfile(folder, '*.png')); % List all PNG files
file_names = natsortfiles({files.name}); % Natural sorting of filenames

n = length(file_names);

% Initialize variables
unique_days = {}; % To store unique days for September
day_counts = [];  % To store counts of data for each day in September

% Loop through all files to extract days and count occurrences for September
for i = 1:n
    month = file_names{i}(34:35); % Extract month part (assuming month is at position 34:35)
    if strcmp(month, '09') % Only process files for September (month == '09')
        day = file_names{i}(36:37); % Extract day part (assuming day is at position 36:37)
        
        % Check if the day is already in the unique_days list
        if isempty(unique_days) || ~ismember(day, unique_days)
            unique_days = [unique_days; day]; % Add new unique day
            day_counts = [day_counts; 1];     % Initialize count for this day
        else
            % Increment count for the existing day
            idx = find(strcmp(unique_days, day));
            day_counts(idx) = day_counts(idx) + 1;
        end
    end
end

% Display results for September
fprintf('Day changes and their data counts for September:\n');
for i = 1:length(unique_days)
    fprintf('Day: %s, Count: %d\n', unique_days{i}, day_counts(i));
end

fprintf('Total unique days in September: %d\n', length(unique_days));

%%
clc; clear all;

% Folder path
folder = 'D:\mj Kim\위성이미지_적외8.7\구름강조(9-11월, 10분단위)';
files = dir(fullfile(folder, '*.png')); % List all PNG files
file_names = natsortfiles({files.name}); % Natural sorting of filenames

n = length(file_names);

% Loop through all files to extract and check hour and minute for Day 03 and Day 04
fprintf('Hour and Minute details for Day 03 and Day 04:\n');
for i = 1:n
    month = file_names{i}(34:35); % Extract month part (assuming month is at position 34:35)
    day = file_names{i}(36:37);   % Extract day part (assuming day is at position 36:37)
    
    if strcmp(month, '09') && (strcmp(day, '03') || strcmp(day, '04'))
        hour = string(file_names{i}(38:39)); % Extract hour part
        min = string(file_names{i}(40:41)); % Extract minute part
        
        fprintf('File: %s | Day: %s | Hour: %s | Minute: %s\n', file_names{i}, day, hour, min);
    end
end