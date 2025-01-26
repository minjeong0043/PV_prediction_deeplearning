clc; clear all; close all;
function file_Rename_inMonth(month_path)
    files = fullfile(month_path, '*.xls*');
    files = dir(files);
    for i = 1:length(files)
    oldFileName = files(i).name;
    oldFilePath = fullfile(month_path, oldFileName);
    data = readtable(oldFilePath, 'FileType','text');

    time = [data{1, 3}];
    y = year(time(:));
    m = month(time(:));
    d = day(time(:));

    newFileName = oldFileName(1:12) +string(y) + sprintf('%02d', m) + sprintf('%02d', d) + '.xls';
    newFilePath = fullfile(month_path, newFileName);
    status = movefile(oldFilePath, newFilePath);

    if status 
        disp(['Success : ',oldFileName,' -->',newFileName]); 
    else
        disp(['Failed : ',oldFileName]);
    end
    end
end

function oneFile_changeTimestep(file_path)
    [folder, file_name, ext] = fileparts(file_path);
    data = readtable(file_path, 'FileType', 'text');

    % startTime = datetime('2020-01-01 00:00', 'Format', 'HH:mm');
    % endTime = datetime('2020-01-01 23:50', 'Format', 'HH:mm');
    startTime = datetime('00:00', 'Format', 'HH:mm');
    endTime = datetime('23:50', 'Format', 'HH:mm');


    setTime = startTime:minutes(10):endTime;
    setTime_str = datestr(setTime, 'HH:MM');
    setTime_str(1,:) = '00:01';

    n = length(data{:,3});
    new_data = {};
    timeIndex = 1;
    dataIndex = 1;

    for i = 1:n
        data_time = datetime(data{i,3}, 'Format', 'HH:mm');
        data_time_str = datestr(data_time, 'HH:MM');
        if data_time_str == setTime_str(timeIndex, :)
            disp(sprintf('data processing . . . (dataIndex : %d) - %s', dataIndex, regexprep(file_name, '[^0-9]', '')));
            new_data(dataIndex, :) = table2cell(data(i, :));
            dataIndex = dataIndex + 1;
            timeIndex = timeIndex + 1;
            if timeIndex > length(setTime_str)
                timeIndex = 1;
            end
        end
    end

    header = {'지점', '지점명', '일시', '기온(°C)', '기온 QC플래그', '누적강수량(mm)', '풍향(deg)',...
    '풍향 QC플래그', '풍속(m/s)', '풍속 QC플래그', '현지기압(hPa)', '현지기압 QC플래그', '해면기압(hPa)',...
    '해면기압 QC플래그', '습도(%)', '습도 QC플래그', '일사(MJ/m^2)', '일조(Sec)'};
    new_data_table = cell2table(new_data, 'variableNames', header);

    output_file = fullfile(folder, [file_name, '_10min', '.xls']);
    disp(['Output file path: ', output_file]);
    writetable(new_data_table, output_file);
    disp(['TimeStep10 data saved to ', output_file]);

    if exist(file_path, 'file') == 2
        delete(file_path);
        disp(['Original file deleted ', file_path]);
    else
        disp('Original file not found');
    end
end


function month_changeTimestep(month_path)
    files = fullfile(month_path, '*.xls*');
    files = dir(files);
    for i = 1:length(files)
        file_path = fullfile(month_path, files(i).name);
        oneFile_changeTimestep(file_path)
    end
end

% folder = 'D:\mj Kim\진행중인 업무\종관기상관측(ASOS)_rawdata\ASOS2020';
% monthFolder = fullfile(folder, 'month*');
% monthFolder = dir(monthFolder);
% 
% for i = 1:12
%     % month = str2num(monthFolder(1).name(6:7));
%     month = str2num(regexprep(monthFolder(i).name, '[^0-9]', ''));
%     disp(['month : ', num2str(month)]);
%     month_path = fullfile(folder, monthFolder(i).name);
%     file_Rename_inMonth(month_path)
% end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Main %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

folder = '\\Ugrid\sml_nas\연구용데이터\종관기상관측(ASOS)';
yearFolder = fullfile(folder, 'ASOS*');
yearFolder = dir(yearFolder);

for y = 1:4
    year = str2num(regexprep(yearFolder(y).name, '[^0-9]', ''))
    disp([' Year : ', num2str(year)]);
    year_path = fullfile(folder, yearFolder(y).name);
    
    % month
    monthFolder = fullfile(year_path, 'month*');
    monthFolder = dir(monthFolder);

    for m = 1:12
        month = str2num(regexprep(monthFolder(m).name, '[^0-9]', ''));
        disp(['month : ', num2str(month)]);
        month_path = fullfile(year_path, monthFolder(m).name);
        % file_Rename_inMonth(month_path);
        month_changeTimestep(month_path);
        
    end
end

