% 报错取消下面注释重试（自动将spm路径加入预设路径），出现有关list的错误请重新添加spm路径，或取消注释下面的行
%或者在命令行输入spm，再重试
% spm('Defaults', 'fMRI');        % 设置SPM默认参数
% spm_jobman('initcfg');          % 初始化作业管理器

% MRI => MNI
% PET => MRI,PET => ROI
ROI = 'Template/Registration/AAL3v1_1mm.nii';
PET = 'PET';
MRI = 'MRI/mri'; %分割后的MRI数据在mri目录下

outputPrefix = 'r'; % 是已经完成的文件前缀
verbose = 0; % 打印SPM输出，检查出错

% 定义日志文件路径
logFile = 'err_coregister.log';

% 打开日志文件（若文件已存在，将追加内容）
fid = fopen(logFile, 'w+');
if fid == -1
    error('无法打开日志文件 %s 进行写入', logFile);
end

% 去除PS打印警告，如果你启动了SPM的Graphic,取消注释去除警告，否则不要这么做
% print('-dpdf', 'output.pdf');

%run
batch_coregiter_job(MNI,ROI,PET,MRI,outputPrefix,verbose,fid);  

function batch_coregiter_job(MNI,ROI,PET,MRI,outputPrefix,verbose,fid,interp)
    if nargin<9
        interp = 4;
    end
    mni = [MNI,',1'];
    roi = [ROI,',1'];
    %%
    % 获取每个目录下的非 r 开头的 .nii 文件
    PET_files = dir(fullfile(PET, '*.nii'));
    MRI_files = dir(fullfile(MRI, '*.nii'));

    processed_files = PET_files(startsWith({PET_files.name}, outputPrefix));
    processed_names = cellfun(@(x) extractAfter(x, strlength(outputPrefix)), {processed_files.name}, 'UniformOutput', false);

    PET_files = PET_files(~(startsWith({PET_files.name}, outputPrefix)));
    PET_files = PET_files(~ismember({PET_files.name}, processed_names));

    fprintf('Total file counts - PET: %d\n',numel(PET_files)+numel(processed_names));
    fprintf('Pending file counts - PET: %d\n',numel(PET_files));

    currentDir = pwd;
    tempName = 'temp.nii';
    rtempName = [outputPrefix,tempName];
    tempFilePath = fullfile(currentDir,tempName);
    rtempFilePath = fullfile(currentDir,rtempName);
    % 遍历 PET 文件并找到匹配的 MRI 文件
    for i = 1:length(PET_files)
        mri_name = ['mwp1',PET_files(i).name]
        MRI_files = dir(MRI); 
        matching_files = MRI_files(startsWith({MRI_files.name}, 'mwp1') ...
            & contains({MRI_files.name}, PET_files(i).name));
        if numel(matching_files) > 0
            mri_name = matching_files(1).name;

        m = fullfile(MRI,mri_name)
        p = fullfile(PET, PET_files(i).name);
        if exist(m)
            for j = 1:length(ROI_files)
                copyfile(p, tempFilePath);
                % 第一步：将 PET 配准到 MRI
                coregister_job(m, tempFilePath, interp, outputPrefix, verbose); 
                movefile(rtempFilePath,tempFilePath);
                % 将 PET 配准到 ROI
                coregister_job(roi, tempFilePath, interp, outputPrefix, verbose); 
                % 重命名配准后的 PET 文件 %% 可以修改自己期望的格式
                % [~, roi_name, ext] = fileparts(roi);
                % cor_pet = sprintf('%s%s_%s%s',outputPrefix,roi_name,PET_files(i).name);
                movefile(rtempFilePath,fullfile(PET,[outputPrefix,PET_files(i).name])); % or  cor_pet   
            end
        else
            fprintf(fid, '未找到与PET匹配的 MRI 文件: %s\n', m);
            warning('未找到与PET匹配的 MRI 文件: %s\n', m);
        end
       fprintf('Done(All): %d(%d),Processing... \n',i,length(PET_files)); 
    end

    delete(tempFilePath);
    % 关闭日志文件
    fclose(fid);
end
