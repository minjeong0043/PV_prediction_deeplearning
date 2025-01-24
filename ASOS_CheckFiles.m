clc; clear all; close all;
% 폴더 경로 설정
%%%%%%%%%%%%%%%%%% Set param %%%%%%%%%%%%%%%
month_num = 9;
folderPath = ['D:\mj Kim\진행중인 업무\종관기상관측(ASOS)\ASOS2023\month' num2str(month_num)];

% 폴더 내 엑셀 파일 목록 가져오기
filePattern = fullfile(folderPath, '*.xls*'); % .xls와 .xlsx 모두 포함
excelFiles = dir(filePattern);

% 파일 목록 확인
if isempty(excelFiles)
    error('폴더 내에 엑셀 파일이 없습니다.');
end

% 결과 저장용 변수 초기화
extractedData = {}; % 각 파일에서 추출한 데이터를 저장

% 파일 읽기 및 데이터 추출
for k = 1:length(excelFiles)
    % 파일 경로 설정
    fileName = excelFiles(k).name;
    fullFilePath = fullfile(folderPath, fileName);
    
    try
        % 엑셀 파일 읽기
        % opts = detectImportOptions(fullFilePath);
        % opts.VariableNamingRule = 'preserve';
        % data = readtable(fullFilePath, opts, 'FileType', 'text');
        data = readtable(fullFilePath, 'FileType', 'text');
        
        % 1행 3열 데이터 추출
        value = data{1, 3}; % 테이블에서 값 추출
        fprintf("파일 읽음: %s, 추출된 값: %s\n", fileName, string(value));

        % 추출한 데이터를 저장
        extractedData{k, 1} = fileName; % 파일 이름
        extractedData{k, 2} = value;    % 추출된 데이터
    catch ME
        % 오류 처리
        fprintf("오류 발생: %s 파일을 읽을 수 없습니다.\n", fileName);
        fprintf("오류 메시지: %s\n", ME.message);
        extractedData{k, 1} = fileName; % 파일 이름만 저장
        extractedData{k, 2} = NaN;      % 추출 실패 시 NaN 저장
    end
end

% 추출 결과 출력
disp('추출된 데이터:');
disp(extractedData);

disp('데이터 길이')
disp(length(extractedData))

%%
end_day_list_2020 = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
end_day_list_2021 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
end_day_list_2022 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
end_day_list_2023 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

month_len = end_day_list_2023(month_num);
date = extractedData(:,2);
dateTimes = [date{:}];
d = day(dateTimes);
missing_day = [];

disp('정해진 길이: ')
disp(end_day_list_2023(month_num))

for i =1: month_len
    isInList = ismember(i, d);
    if isInList == 0
        missing_day = [missing_day, i];
    end
end

disp('missing_list = ')
disp(missing_day)

