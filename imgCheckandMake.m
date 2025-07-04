clc; clear all; close all;
function return_num = imgCheckandMake(return_num,folder)
    return_num = 1;
    files = dir(fullfile(folder, '*.png')); % 폴더 내 PNG 파일 목록 가져오기
    files = natsortfiles({files.name}); % 자연 정렬

    % 시간 및 분 단위 배열 정의
    hour_index = ["15", "16", "17", "18", "19", "20", "21", "22", "23", ...
                  "00", "01", "02", "03", "04", "05", "06", "07", "08", ...
                  "09", "10", "11", "12", "13", "14"];
    min_index = ["00", "10", "20", "30", "40", "50"]; 
    n = length(files); 
    index_h = 0; index_m = 0; index_m_new = 0; index_h_new = 0;

    h = 1; 
    j=0;
    for i = 1:n
        hour = string(files{i}(37:38)); 
        min = string(files{i}(39:40)); 

        expected_min = min_index(mod(i-1, 6)+1);

        if hour ~= hour_index(h)
            fprintf('HOUR) Missing file before: %s\n', files{i}); 
            % 파일 만들기
            % i = 4
            oldFileName = files{i-1};
            % oldFilePath에서 10분 더하기 (파일명에 따라 index 변경해줘야함)
            index_h = find(hour_index == oldFileName(37:38));
            index_m = find(min_index == oldFileName(39:40));
            index_m = index_m;
            index_h_new = index_h;
            index_m_new = index_m+1;
            if index_m_new > length(min_index)
                index_m_new = 1;
                index_h_new = index_h + 1;
                if index_h_new > length(hour_index)
                    index_h_new = 1;
                end
            end
            % 파일 이름에따라 index 변경해줘야함.
            FilePath = [folder, oldFileName(1:36)]
            newFilePath = string(FilePath)+hour_index(index_h_new)+min_index(index_m_new)+'_' + hour_index(index_h)+min_index(index_m)+'.png';
            copyfile(fullfile(folder, oldFileName), newFilePath);
            if exist(newFilePath)
                fprintf('~~~Making files : %s\n', newFilePath);
                return_num = 0;
            end
            break; 
        else
            if expected_min ~= min
                fprintf('MIN) Missing file before: %s\n', files{i});
                % 파일 만들기
                % i = 4
                oldFileName = files{i-1};
                % oldFilePath에서 10분 더하기
                index_h = find(hour_index == oldFileName(37:38));
                index_m = find(min_index == oldFileName(39:40));
                index_m = index_m;
                index_h_new = index_h;
                index_m_new = index_m+1;
                if index_m_new > length(min_index)
                    index_m_new = 1;
                    index_h_new = index_h + 1;
                    if index_h_new > length(hour_index)
                        index_h_new = 1;
                    end
                end

                FilePath = [folder, oldFileName(1:36)]
                newFilePath = string(FilePath)+hour_index(index_h_new)+min_index(index_m_new)+'_' + hour_index(index_h)+min_index(index_m)+'.png';
                copyfile(fullfile(folder, oldFileName), newFilePath);
                if exist(newFilePath)
                    fprintf('@@@@@Making files : %s\n', newFilePath);
                    return_num = 0;
                end
                j = j+3;
                % h = h-1;
                break;
            end
        end

        if expected_min == "50"
            h = h + 1;
            if h > length(hour_index) 
                h = 1;
            end
        end
    end
end


%% main
folder = '\\Ugrid\sml_nas\연구용데이터\태풍이미지\13.장미_(전처리, 누락데이터)\';
return_num = 0
return_num = imgCheckandMake(return_num, folder);

fprintf('File check completed.\n');


%%
counter = 0;
list = dir(fullfile(folder, '*.png'))
n = size(list)
while counter < n(1)
    return_num = imgCheckandMake(return_num, folder);
    fprintf("File check completed.\n")
    % pause(2);
    counter = counter + 1;
    fprintf("counter : %d\n", counter);
end

fprintf("Finished Checking")
