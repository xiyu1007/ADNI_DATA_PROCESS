function flip_nii(output_nii,input_nii)
    if nargin <1 output_nii = 'output.nii'; end
    if nargin < 2
        p=spm_select(1,'.nii');
        if size(p,1) <= 0
            return
        end
        f=strtrim(p(1,:));
        input_nii = deblank(f); %删除路径末尾空白字符
    end

    V = spm_vol(input_nii);

    % V.mat(1,1) = -V.mat(1,1);  % 翻转 x 方向
    % V.mat(1,4) = -V.mat(1,4);  % 反转原点的 x 坐标 V.mat(1,4)
    data = spm_read_vols(V);   % 读取数据，在更改name之前
    % epsilon = 0.2; % 定义一个很小的正数作为容差
    % data(abs(data - 1.0000) > epsilon) = 0; % 将所有与1.0的差的绝对值大于epsilon的值设置为0
    data = flip(data, 1);      % 沿 X 轴（第一个维度）翻转数据
    % 平移数据，沿 X 轴平移 10 个单位
    % 使用 circshift 或者手动调整数据的位置

    % 使用 circshift 平移数据
    data = circshift(data, [0, 0, 0]);
    
    % 如果数据已经平移，则更新空间变换矩阵中的原点坐标
    V.mat(1:1,4) = 0;
    V.fname = output_nii; 

    spm_write_vol(V, data);  % 写入新的文件必须有V，和data，data = spm_read_vols(V)
    spm_image('Display', output_nii);  % 显示修改后的模板
end


