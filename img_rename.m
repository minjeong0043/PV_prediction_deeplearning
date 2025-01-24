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


folder = 'D:\mj Kim\진행중인 업무\종관기상관측(ASOS)_rawdata\ASOS2020';
monthFolder = fullfile(folder, 'month*');
monthFolder = dir(monthFolder);

for i = 1:12
    % month = str2num(monthFolder(1).name(6:7));
    month = str2num(regexprep(monthFolder(i).name, '[^0-9]', ''));
    disp(['month : ', num2str(month)]);
    month_path = fullfile(folder, monthFolder(i).name);
    file_Rename_inMonth(month_path)
end



