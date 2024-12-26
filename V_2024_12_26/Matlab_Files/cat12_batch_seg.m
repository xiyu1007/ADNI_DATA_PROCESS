% 分割出现任何错误请尝试去除所有SPM路径再添加后重试
% 若还是不行则，重新安装最新SPM,注意记得备份cat12，否则记得重新下载cat12
% 使用示例
% 输入目录
inputDir = 'D:\_DATASETS\Filter\ADNI2\DICOM2Nii\MRI';    
% mask = 'template/ROITemplate/aal3.nii'; % ROI模板

nproc = 6;  % 电脑核心数，每次处理的文件数量

prefix = ''; %筛选需要分割的nii，若MRI未配准

%run
batch_cat12_seg_job(inputDir, nproc,prefix);  % 执行批处理

function batch_cat12_seg_job(inputDir,nproc,prefix)
    % 输入参数：
    %   inputDir: 包含 NIfTI 文件的目录
    %   nproc: 每次传入 run_spm_job 的文件数量
    %   filter_cat_seg: 已处理文件的目录结构数组

    % 获取所有 NIfTI 文件
    niftiFiles = dir(fullfile(inputDir, [prefix '*.nii']));
    numFiles = length(niftiFiles);
    if numFiles == 0
        fprintf('Number of unprocessed files: %d\n', numFiles);
        return
    end
    % 初始化 keepIndices 以保留未处理文件
    keepIndices = true(numFiles,1);
    fprintf('Filter processed files...\n')
    % 遍历每个文件并检查是否已处理
    %过滤已经完成的数据
    %y_是已经完成的文件前缀，不要修改，不会改变输出的前缀,和prefix无关
    filter_seg_dir = fullfile(inputDir,'mri');
    filter_cat_seg = dir(fullfile(filter_seg_dir, 'y_*.nii'));
    filter_xml_dir = fullfile(inputDir,'label');
    filter_cat_xml = dir(fullfile(filter_xml_dir, 'catROI_*.xml'));
    if size(filter_cat_seg,1)>0 && size(filter_cat_xml,1) > 0
        for i = 1:numFiles
            [~,xml_mane] = fileparts(niftiFiles(i).name);
            if ismember(['y_',niftiFiles(i).name], {filter_cat_seg.name}) ...
                && ismember(['catROI_',xml_mane,'.xml'], {filter_cat_xml.name})

                keepIndices(i,1) = false;  % 如果文件已处理，则排除
            end
        end
    end
    niftiFiles = niftiFiles(keepIndices);  % 保留未处理的文件
    numFiles = length(niftiFiles);  % 更新未处理文件数量
    fprintf('Number of filter files: %d\n', sum(~keepIndices))
    fprintf('Number of unprocessed files: %d\n', numFiles)
    if numFiles == 0
        return
    end

    % 创建文件路径的元胞数组，每个文件路径作为单独的元胞数组元素
    inputFiles = cell(numFiles, 1);
    for i = 1:numFiles
        % 使用完整路径并添加 ',1' 后缀
        inputFiles{i} = fullfile(inputDir, [niftiFiles(i).name, ',1']);
    end
    % 运行任务
    cat12_seg_job(inputFiles,nproc);

end
