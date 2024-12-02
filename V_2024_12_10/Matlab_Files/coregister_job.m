function coregister_job(ref,source,interp,outputPrefix,verbose)
    if nargin < 4 || isempty(outputPrefix)
        prefix = 'r';
    end
    if nargin < 5
        verbose = true;
    end
    % 创建 matlabbatch 结构体
    matlabbatch{1}.spm.spatial.coreg.estwrite.ref = {ref}; % 设置参考图像
    matlabbatch{1}.spm.spatial.coreg.estwrite.source = {source}; % 设置源图像
    matlabbatch{1}.spm.spatial.coreg.estwrite.other = {''}; % 空白，表示没有其他图像
    matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi'; % 使用 NMI 作为成本函数
    matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2]; % 配准分辨率：4mm 和 2mm
    matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001]; % 容差
    matlabbatch{1}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7]; % 平滑处理：7mm
    matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.interp = interp; % 四次插值
    matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0]; % 不进行卷绕
    matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.mask = 0; % 不应用掩膜
    matlabbatch{1}.spm.spatial.coreg.estwrite.roptions.prefix = outputPrefix; % 设置输出文件前缀
    % 运行任务
    % 使用 evalc 执行 spm_jobman 命令，抑制打印输出
    if verbose
        spm_jobman('run', matlabbatch); % 执行配准任务
    else
        evalc('spm_jobman(''run'', matlabbatch);');
    end
end

