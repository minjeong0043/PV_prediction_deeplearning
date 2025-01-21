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
            oldFilePath = fullfile(folder, files{i-1});
            % oldFilePath에서 10분 더하기
            index_h = find(hour_index == oldFilePath(79:80));
            index_m = find(min_index == oldFilePath(81:82));
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

            newFilePath = string(oldFilePath(1:78))+hour_index(index_h_new)+min_index(index_m_new)+'_' + hour_index(index_h)+min_index(index_m)+'.png';
            copyfile(oldFilePath, newFilePath);
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
                oldFilePath = fullfile(folder, files{i-1});
                % oldFilePath에서 10분 더하기
       
                index_h = find(hour_index == oldFilePath(79:80));
                index_m = find(min_index == oldFilePath(81:82));
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

                newFilePath = string(oldFilePath(1:78))+hour_index(index_h_new)+min_index(index_m_new)+'_' + hour_index(index_h)+min_index(index_m)+'.png';
                copyfile(oldFilePath, newFilePath);
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
folder = 'E:\PV_forecast_2024\적외선_8.7(2021년, 10분단위)';
return_num = 0
return_num = imgCheckandMake(return_num, folder);

fprintf('File check completed.\n');
 

%%
counter = 0;
while counter < 300
    return_num = imgCheckandMake(return_num, folder);
    fprintf("File check completed.\n")
    % pause(2);
    counter = counter + 1;
    fprintf("counter : %d\n", counter);
end