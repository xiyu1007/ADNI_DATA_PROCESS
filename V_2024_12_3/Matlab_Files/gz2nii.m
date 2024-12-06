% 指定输入和输出路径
input_file = 'template\'; % 替换为你的 .nii.gz 文件路径
output_file = '';         % 输出的 .nii 文件路径

% 解压缩 .nii.gz 文件
gunzip(input_file);

% 提示用户
disp(['Converted ' input_file ' to ' output_file]);
