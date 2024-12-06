function [] = Fun_Split_4DTo3D(root_dir,output_dir,volume_to_keep)
   
   % 初始化一个表来存储数据
    results = table();
    % 获取所有的 NIfTI 文件
    nii_files = dir(fullfile(root_dir, '**', '*.nii'));  % 遍历所有子目录

    % 遍历每个 NIfTI 文件
    fprintf('Processing 4D file...\n');
    for i = 1:length(nii_files)
        % 获取文件的完整路径
        nii_path = fullfile(nii_files(i).folder, nii_files(i).name);
        % 使用原始文件名的一部分作为新文件名
        [~, Modality, ~] = fileparts(nii_files(i).folder); % 获取最后一级目录名称
        m_out_dir = fullfile(output_dir,Modality);
        if ~exist(m_out_dir, 'dir')
            mkdir(m_out_dir); % 创建文件夹，若已存在则跳过
        end
        
        [~, name, ~] = fileparts(nii_files(i).name);
        % 加载文件信息
        V = spm_vol(nii_path);

        % 检查是否为 4D 文件
        if numel(V) > 1
            % fprintf('Processing 4D file: %s\n', nii_path);
            % 拆分 4D 文件
            Vo = spm_file_split(nii_path);

            if volume_to_keep > numel(Vo)
                fprintf('volume_to_keep:%d > numel(Vo):%d\n', volume_to_keep, numel(Vo));
                return
            end
           
            % 只保留指定卷并删除其他卷
            for j = 1:numel(Vo) 
                old_filename = Vo(j).fname;  % 原始文件名
                if volume_to_keep == 0 && ~isempty(output_dir)
                    [~, name, ~] = fileparts(Vo(j).fname);
                    new_filename = fullfile(m_out_dir,strcat(name,'.nii'));  % 新文件名
                    movefile_with_error_handling(old_filename, new_filename)
                % 只保留指定卷
                elseif  j == volume_to_keep
                    % 确定输出目录
                    if isempty(output_dir)
                        output_dir = nii_files(i).folder;  % 使用原文件目录
                    end
                    new_filename = fullfile(m_out_dir,strcat(name,'.nii'));  % 新文件名
                    movefile_with_error_handling(old_filename, new_filename)

                else
                    delete_with_error_handling(old_filename)
                end
            end
            results = [results; table({name}', {Modality}', 'VariableNames', {'Subject', 'Modality'})];
        else
            new_filename = fullfile(m_out_dir,strcat(name,'.nii'));  % 新文件名
            copyfile(nii_path, new_filename);
        end
        

    end
    fprintf('Over Processing 4D file...\n');
    % 将结果写入 CSV 文件
    writetable(results, fullfile(output_dir, 'Split_4DTo3D.csv'));
end


function movefile_with_error_handling(old_filename, new_filename)
    try
        movefile(old_filename, new_filename);
    catch ME
        fprintf('Error renaming %s to %s: %s\n', old_filename, new_filename, ME.message);
    end
end

function delete_with_error_handling(old_filename)
    try
        delete(old_filename);
    catch ME
        fprintf('Error deleting %s: %s\n', old_filename, ME.message);
    end
end