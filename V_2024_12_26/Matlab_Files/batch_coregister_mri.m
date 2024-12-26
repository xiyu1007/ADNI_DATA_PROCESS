% 报错取消下面注释重试（自动将spm路径加入预设路径），出现有关list的错误请重新添加spm路径，或取消注释下面的行
%或者在命令行输入spm，再重试
% spm('Defaults', 'fMRI');        % 设置SPM默认参数
% spm_jobman('initcfg');          % 初始化作业管理器
% MRI => MNI
% PET => MRI,PET => ROI
MNI = 'Template/Registration/mni_icbm152_t1_tal_nlin_asym_09c.nii';
MRI = 'D:\_DATASETS\Filter\ADNI1\DICOM2Nii\MRI';  

outputPrefix = 'r'; % 是已经完成的文件前缀
verbose = 0; % 打印SPM输出，检查出错

% 去除PS打印警告，如果你启动了SPM的Graphic,取消注释去除警告，否则不要这么做
% print('-dpdf', 'output.pdf');

%run
batch_coregiter_job(MNI,MRI,outputPrefix,verbose);  

function batch_coregiter_job(MNI,MRI,outputPrefix,verbose,interp)
    if nargin<5 interp = 4; end

    % 获取每个目录下的非 r 开头的 .nii 文件
    mni = [MNI,',1'];
    %%
    MRI_files = dir(fullfile(MRI, '*.nii'));

    processed_files = MRI_files(startsWith({MRI_files.name}, outputPrefix));
    processed_names = cellfun(@(x) extractAfter(x, strlength(outputPrefix)), {processed_files.name}, 'UniformOutput', false);

    MRI_files = MRI_files(~startsWith({MRI_files.name}, outputPrefix));
    MRI_files = MRI_files(~ismember({MRI_files.name}, processed_names));


    fprintf('Total file counts - MRI: %d\n',numel(MRI_files)+numel(processed_names));
    fprintf('Pending file counts - MRI: %d\n',numel(MRI_files));

    currentDir = pwd;
    tempName = 'temp.nii';
    rtempName = [outputPrefix,tempName];
    tempFilePath = fullfile(currentDir,tempName);
    rtempFilePath = fullfile(currentDir,rtempName);

    for i = 1:numel(MRI_files)
        m = fullfile(MRI, MRI_files(i).name);
        % copyfile(m, tempFilePath);
        coregister_job(mni,m, interp, outputPrefix,verbose); % 将 MRI 配准到 MNI
        % movefile(rtempFilePath,fullfile(MRI,[outputPrefix,MRI_files(i).name])); 
        fprintf('Done(All): %d(%d),Processing... \n',i,numel(MRI_files)); 
    end
    delete(tempFilePath);
end



