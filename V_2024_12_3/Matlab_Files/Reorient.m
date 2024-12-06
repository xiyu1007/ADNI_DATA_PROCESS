% 报错取消下面注释重试（自动将spm路径加入预设路径）
% spm('Defaults', 'fMRI');        % 设置SPM默认参数
% spm_jobman('initcfg');          % 初始化作业管理器

p=spm_select(Inf,'.nii');
i_type = 't1'; % use default: T1canonical, MRI：t1/t2
% i_type = 'pet'; % use default: T1canonical, MRI：t1/t2
center_origin = true;

% 打开文件以追加写入（如果文件不存在则创建）
logFile = 'Failed_auto_reorient.txt';
fid = fopen(logFile, 'w+'); % 'w' 模式
if fid == -1
    error('Cannot open log file: %s', logFile);
end

%% RUN
auto_reorient(p,i_type,center_origin,fid)


%%
function auto_reorient(p,i_type,center_origin,fid) 
    % 检查输入
    if nargin<1 || isempty(p)
        return
    end
    if iscell(p), p = char(p); end
    Np = size(p,1);
    
    if nargin<2 || isempty(i_type)
        i_type = 'T1canonical';
    end
    
    if nargin<3
        center_origin = true;
    end


    %% 指定模板
    switch lower(i_type)
        case 't1',
            tmpl = fullfile(spm('dir'),'toolbox','OldNorm','T1.nii');
        case 't2', 
            tmpl = fullfile(spm('dir'),'toolbox','OldNorm','T2.nii');
        case 'epi', 
            tmpl = fullfile(spm('dir'),'toolbox','OldNorm','EPI.nii');
        case 'pd', 
            tmpl = fullfile(spm('dir'),'toolbox','OldNorm','PD.nii');
        case 'pet', 
            tmpl = fullfile(spm('dir'),'toolbox','OldNorm','PET.nii');
        case 'spect', 
            tmpl = fullfile(spm('dir'),'toolbox','OldNorm','SPECT.nii');
        case 't1canonical', 
            tmpl = fullfile(spm('dir'),'canonical','single_subj_T1.nii');
        otherwise, error('未知的图像类型')
    end

    %读取模板
    vg=spm_vol(tmpl);
    flags.regtype='rigid';
    %p=spm_select(inf,'image');
    num_err = 0;
    num_done = 0;
    for i=1:size(p,1)
        f=strtrim(p(i,:));
        if center_origin
            %% Set the origin to the center of the image
            % 将图像ac设置到图像中心.
            file = deblank(f); %删除路径末尾空白字符
            st.vol = spm_vol(file);%存储在结构体 st.vol 中
            vs = st.vol.mat\eye(4);%计算图像空间中的坐标变换矩阵 vs
            %将变换矩阵 vs 的最后一列（表示平移）设置为图像维度的中心坐标。
            % st.vol.dim 是图像的维度（例如，[x, y, z]）
            vs(1:3,4) = (st.vol.dim+1)/2; 
            %用于设置或获取图像空间的信息的函数。这里，它被用来更新图像的空间变换信息。
            %使用 inv(vs)（vs 的逆矩阵）将图像的空间信息更新到其文件中。
            spm_get_space(st.vol.fname,inv(vs)); 
        end
        try
            spm_smooth(f,'temp.nii',[12 12 12]);
            vf=spm_vol('temp.nii');
            [M,scal] = spm_affreg(vg,vf,flags);
            M3=M(1:3,1:3);
            [u s v]=svd(M3);
            M3=u*v';
            M(1:3,1:3)=M3;
            N=nifti(f);
            N.mat=M*N.mat;
            create(N);
            % fprintf('Successfully processed file: \n%s\n',f);
            num_done = num_done + 1;
            fprintf('processing file Done(All): %d(%d)\n',num_done,size(p,1));
            success = true;  
        catch ME
            num_err = num_err + 1;
            fprintf('Failed to process file: \n%s\n',f)
            fprintf('Failed to process file: \n%s\n',ME.message)
            fprintf(fid, 'Failed to process file:\n%s\n', f); % 写入失败信息到文件
            fprintf(fid, '\n'); % 换行
            fprintf(fid, repmat('=', 1, 20)); % 写入20个等号
        end
    end
    fprintf('Number of file successed to process: %d\n',size(p,1))
    fprintf('Number of file Failed to process: %d\n',num_err)
    delete('temp.nii');
    % 关闭日志文件
    fclose(fid);
end


