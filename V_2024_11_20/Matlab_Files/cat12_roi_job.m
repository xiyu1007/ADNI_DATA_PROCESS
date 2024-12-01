% run_spm_job.m
% 此文件用于调用和运行 SPM 批处理任务

% 设置根目录
rootDir = 'D:\Matlab\Project\GroupMeeting\Fun_Pre_Processing\Bias_MRI\label';
outputDir = 'D:\\Matlab\\Project\\GroupMeeting\\Fun_Pre_Processing\\Output';

% 获取根目录下的所有 XML 文件
xmlFiles = dir(fullfile(rootDir, '*.xml'));
% 初始化一个元胞数组以存储所有 XML 文件路径
roi_xml_paths = cell(length(xmlFiles), 1);  % 预分配列元胞数组
% 遍历每个 XML 文件并设置批处理参数
for i = 1:length(xmlFiles)
    % 获取 XML 文件的完整路径
    xmlFilePath = fullfile(rootDir, xmlFiles(i).name);
    % 将当前 XML 文件路径添加到元胞数组
    roi_xml_paths{i} = xmlFilePath;  % 直接赋值
end

% 初始化批处理变量
matlabbatch = {};
% 设置批处理参数
matlabbatch{1}.spm.tools.cat.tools.calcroi.roi_xml = roi_xml_paths;  % 将所有路径传入
matlabbatch{1}.spm.tools.cat.tools.calcroi.point = '.';
matlabbatch{1}.spm.tools.cat.tools.calcroi.outdir = {outputDir};
matlabbatch{1}.spm.tools.cat.tools.calcroi.calcroi_name = 'ROI';

% 运行批处理任务
spm('defaults', 'FMRI');  % 初始化 SPM 默认设置
spm_jobman('run', matlabbatch);  % 执行批处理任务
