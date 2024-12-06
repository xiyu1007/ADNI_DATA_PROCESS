% 指定NIfTI文件夹路径
% 替换为你的NIfTI文件夹路径
nii_folder = ...
'MRI\mri'; 
pasue_time = 0; % 0 To enter
Quick_View_All_nii(nii_folder,pasue_time)



function Quick_View_All_nii(nii_folder,pasue_time)
    % 初始化SPM
    spm('Defaults', 'fMRI');        % 设置SPM默认参数
    spm_jobman('initcfg');          % 初始化作业管理器
    pause(2);
    % 获取该文件夹下所有NIfTI文件
    all_files = dir(fullfile(nii_folder, '*.nii'));
    
    % 遍历每个文件
    for i = 1:length(all_files)
        % 构建文件完整路径
        nii_file = fullfile(nii_folder, all_files(i).name);
        
        % 显示NIfTI图像
        spm_image('Display', nii_file);
        fprintf("All(include No nii): %d\t, Now: %d\n",length(all_files),i)
        % 等待用户按下回车键
        if pasue_time
            pause(pasue_time);
        else
            user_input = input('按 "q" 并回车退出，按回车键继续: ', 's');
            if strcmp(user_input, 'q')
                disp('程序终止。');
                break;
            end
        end
    end
    
    % 关闭当前图像窗口
    spm_figure('Close', gcf); % 关闭当前图像窗口
    close all; % 关闭所有图像窗口
end