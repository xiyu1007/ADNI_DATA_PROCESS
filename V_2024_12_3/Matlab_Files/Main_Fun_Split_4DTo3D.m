% 分割4D图像

% 指定根目录
root_dir = "D:\Matlab\Project\GroupMeeting\Datasets_Pre_Processing\Filter\ADNIGO\DICOM2Nii"; 

% 指定输出目录
% 空则覆盖原文件！！！
output_dir = 'D:\Matlab\Project\GroupMeeting\Datasets_Pre_Processing\AC-PC\ADNIGO';  
% output_dir = [];  
if ~isempty(output_dir) && ~exist(output_dir, 'dir')
    mkdir(output_dir);  % 如果输出目录不存在，创建目录
end

% TODO
volume_to_keep=1; % 0则保留所有volume

Fun_Split_4DTo3D(root_dir,output_dir,volume_to_keep)