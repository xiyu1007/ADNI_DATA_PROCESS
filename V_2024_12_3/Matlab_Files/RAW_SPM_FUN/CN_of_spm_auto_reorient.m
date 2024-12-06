function spm_auto_reorient(p,i_type,p_other) 

% FORMAT spm_auto_reorient(p,i_type,p_other)
%
% 函数用于自动（但近似地）刚体重新定位
% T1 图像（或任何其他常用图像模态）到 MNI 空间，
% 主要是设置 AC 位置并校正头部旋转，
% 以便进一步进行图像的分割/归一化。
% 这很有用，因为“统一分割”过程对图像的初始方向
% 相当敏感。
%
% 如果选择了多个图像，则它们应全部为
% *相同* 的模态。此外，每个图像将被 *单独* 处理。
% 因此，不应对整个 fMRI 时间序列应用自动重新定位！
% 在 fMRI 时间序列的情况下，使用平均 MRI 作为第一个
% 参数，并将所有其他图像放入第二个参数的单元格中（见
% 下文）。
%
% 输入：
% - p       : 要重新定位的图像的文件名或文件名列表
% - i_type  : 图像类型 'T1'（默认），'T2'，'PET'，'EPI'，... 即 
%             SPM 提供的任何模板
% - p_other : 其他需要与相应的 p 图像一起重新定位的图像文件名的
%             单元数组。应与 p 的长度相同，或留空（默认）。
%
% 输出：
% - 修改所选图像的头文件，其他图像也会被修改（如果有指定的话）。
%__________________________________________________________________________
% 版权所有 (C) 2011 Cyclotron Research Centre

% 原代码由 Carlton Chu 编写，FIL, UCL, London, UK
% Christophe Phillips 修改和扩展，CRC, ULg, Liege, Belgium

%% 检查输入
if nargin<1 || isempty(p)
    return
    p = spm_select(inf,'image');
end
if iscell(p), p = char(p); end
Np = size(p,1);

if nargin<2 || isempty(i_type)
    i_type = 'T1canonical';
end

if nargin<3 || isempty(p_other{1})
    p_other = cell(Np,1);
end
if numel(p_other)~=Np
    error('crc:autoreorient','其他图像的数量不正确！');
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
vg = spm_vol(tmpl);
flags.regtype = 'rigid';

%% 一次处理每个图像 p
for ii = 1:Np
    % 获取图像并平滑处理
    f = strtrim(p(ii,:));
    spm_smooth(f,'temp.nii',[12 12 12]);
    vf = spm_vol('temp.nii');
    % 估计重新定位
    [M, scal] = spm_affreg(vg,vf,flags);
    M3 = M(1:3,1:3);
    [u s v] = svd(M3);
    M3 = u*v';
    M(1:3,1:3) = M3;
    % 应用于图像 p
    N = nifti(f);
    N.mat = M*N.mat;
    create(N);
    % 应用于其他图像
    No = size(p_other{ii},1);
    for jj = 1:No
        fprintf("Processing %dth nii file\n",jj)
        %%
        fo = strtrim(p_other{ii}(jj,:));
        if ~isempty(fo) && ~strcmp(f,fo)
            % 允许以下情况：
            % - 传入了空名称 
            % - 名称与用于重新定位的图像相同
            % => 跳过
            spm_smooth(fo,'temp.nii',[12 12 12]);
            vf = spm_vol('temp.nii');
            % 估计重新定位
            [M, scal] = spm_affreg(vg,vf,flags);
            M3 = M(1:3,1:3);
            [u s v] = svd(M3);
            M3 = u*v';
            M(1:3,1:3) = M3;
            % 应用于图像 p
            N = nifti(fo);
            N.mat = M*N.mat;
            create(N);
        end
    end
    % 清理临时文件
    delete('temp.nii');
    disp("Processing Over!")
end

end


% % 测试 
p = spm_select(1,'nii');
pt = spm_select(Inf,'nii');
p_other = {pt};
% i_type = []; % use default
% i_type = 'T1'; % use default
i_type = 'pet'; % use default
spm_auto_reorient(p,i_type,p_other)

