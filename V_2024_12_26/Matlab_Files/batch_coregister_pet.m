% 报错取消下面注释重试（自动将spm路径加入预设路径），出现有关list的错误请重新添加spm路径，或取消注释下面的行
%或者在命令行输入spm，再重试
% spm('Defaults', 'fMRI');        % 设置SPM默认参数
% spm_jobman('initcfg');          % 初始化作业管理器

% MRI => seg MRI (MRI/mri)
% PET => MRI,PET => MNI(def spital register)
PET = 'D:\_DATASETS\Filter\ADNI2\DICOM2Nii\PET';
MRI = 'D:\_DATASETS\Filter\ADNI2\DICOM2Nii\MRI\mri'; %分割后的MRI数据在mri目录下

outputPrefix = 'wr'; % 是已经完成的文件前缀
verbose = 0; % 打印SPM输出，检查出错
interp = 1;

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
batch_coregiter_job(PET,MRI,outputPrefix,verbose,fid);  

function batch_coregiter_job(PET,MRI,outputPrefix,verbose,fid,interp)
    if isempty(outputPrefix) outputPrefix = 'wr'; end
    if nargin<6
        interp = 1;
    end
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
        %% 
        [~,subject_id,~] = fileparts(PET_files(i).name);
        seg_mri_name = ['p0',PET_files(i).name];
        % seg_mri_name = ['p0','r',PET_files(i).name]
        %%
        MRI_files = dir(MRI); 
        matching_files = MRI_files(startsWith({MRI_files.name}, 'p0') ...
            & contains({MRI_files.name}, subject_id));
        if numel(matching_files) > 0
            seg_mri_name = matching_files(1).name;
        end
        mri_name = extractAfter(seg_mri_name, strlength('p0'));
        def = ['y_', mri_name];

        m = fullfile(MRI,seg_mri_name);
        p = fullfile(PET, PET_files(i).name);
        d = fullfile(MRI,def);
        if exist(m) & exist(d)
            copyfile(p, tempFilePath);
            % 第一步：将 PET 配准到 mwp1MRI
            coregister_job(m, tempFilePath, interp, outputPrefix, verbose); 
            copyfile(rtempFilePath, tempFilePath);
            normalise_job(d,tempFilePath,interp,outputPrefix,verbose);
            % cor_pet = sprintf('%s%s_%s%s',outputPrefix,roi_name,PET_files(i).name);
            movefile(rtempFilePath,fullfile(PET,[outputPrefix,PET_files(i).name])); % or  cor_pet
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
