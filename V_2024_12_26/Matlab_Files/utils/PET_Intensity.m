% NO Complete!!!
clc,clear;
roi = 'test/aal3.nii';
pet = 'test';
s_info = 'Info/Web_BOTH_MRI_PET.csv';
get_pet_data(roi,pet,'',s_info)
function get_pet_data(mask_path,pet_dir,roi_info,subject_info,Vox_mm3,SUVr,cerebellar,startswith,output_csv)
    if nargin < 4 subject_info = ''; end
    if nargin < 6 SUVr = 1; end
    if nargin < 5 Vox_mm3 = 1; end
    if nargin < 7 cerebellar = 0; end
    if nargin < 8 startswith = 'wr'; end
    if nargin < 9 output_csv = 'PET_DATA.csv'; end

    % 初始化参数
    ID = 'Subject ID';
    Injected_dose = 185;  % MBq, FDG-PET Reference ADNI
    cerebellar_ID = 95:112;  % 小脑区域ID
    % cerebellar_ID = 95:120;  % 小脑区域ID

    roi_info = load_roi_info('Template/ROITemplate/aal3.csv',1,';');
    header = get_header(roi_info, Vox_mm3, SUVr);
    if SUVr
        if ~isempty(subject_info)
            % s_info = readtable(subject_info,'VariableNamingRule','preserve');
            s_info = readtable(subject_info, 'VariableNamingRule', 'preserve', 'TreatAsEmpty', {'NA', 'N/A', ''});
            s_info = s_info(strcmp(s_info.Modality, 'PET'), :);
        else
            disp('计算SUVr时需要输入subject_info（体重）参数');
            return;
        end
    end
    
    % 打开输出文件
    fid = fopen(output_csv, 'w');
    % 获取nii文件列表
    nii_files = dir(fullfile(pet_dir, [startswith, '*.nii*']));
    

    header = get_header(roi_info, Vox_mm3, SUVr);
    fprintf(fid, '%s\n', strjoin(header, ';'));

    mask = niftiread(mask_path);
    roi_V = spm_vol(mask_path);
    data = spm_read_vols(roi_V); % 读取数据，在更改name之前
    roi_affine  = roi_V.mat;
    unique_values = unique(mask(mask ~= 0));  % 获取唯一的mask值，排除0
    indices = find(data == 1);
    [rows, cols, slices] = ind2sub(size(data), indices);
    % 如果需要将索引转换为物理空间坐标，可以使用仿射矩阵
    % 假设你想获取物理坐标 (x, y, z)
    inverse_affine = inv(roi_affine);
    physical_coords = roi_affine * [rows'; cols'; slices'; ones(1, numel(rows))];
    % physical_coords(1, :) 是 x 坐标，physical_coords(2, :) 是 y 坐标，physical_coords(3, :) 是 z 坐标
    voxel_coords = inverse_affine * [physical_coords];
    % intensity = nii(sub2ind(size(nii), rows, cols, slices));
    for i = 1:length(nii_files)

        ce_suv = 1;
        weight = -1;

        nii_filename = nii_files(i).name;
        nii_path = fullfile(pet_dir, nii_filename);
        nii = niftiread(nii_path);  % 读取NIfTI文件

        indices = find(mask == ci);

        
        % 计算SUVr
        if SUVr
            [~, sid] = fileparts(nii_filename);
            sid = sid(length(prefix)+1:end);  % 获取subject ID
            weight_idx = strcmp(s_info.(ID), sid);
            if any(weight_idx)
                weight = s_info.Weight(weight_idx) * 1000;  % 体重以克为单位
            else
                disp([sid, ' 没有体重信息，SUVr可能为0']);
            end
            
            sum_ce = 0;
            for ci = cerebellar_ID
                indices = find(mask == ci);
                ce_vox_in = nii(indices);  % 获取小脑区域的体素值
                sum_ce = sum_ce + sum(ce_vox_in);
            end
            ce_suv = sum_ce / (Injected_dose / weight);
        end
        
        % 计算每个ROI的平均值和其他特征
        average_values = {};
        for value = fieldnames(roi_info)'
            value = value{1};
            avg_intensity = 0;
            vox_mm3 = 0;
            roi_suvr = 0;
            
            if ~ismember(value, unique_values) || (ismember(value, cerebellar_ID) && ~cerebellar)
                continue;
            else
                indices = find(mask == value);
                intensity = nii(indices);
                avg_intensity = mean(intensity);
                sum_intensity = sum(intensity);
                
                vox_mm3 = numel(indices);
                roi_suv = sum_intensity / (Injected_dose / weight);
                roi_suvr = roi_suv / ce_suv;
            end
            
            average_values = [average_values, {num2str(avg_intensity)}];
            if Vox_mm3
                average_values = [average_values, {num2str(vox_mm3)}];
            end
            if SUVr
                average_values = [average_values, {num2str(roi_suvr)}];
            end
        end
        
        % 写入CSV
        fprintf(fid, '%s,%s\n', nii_filename, strjoin(average_values, ','));
    end
    
    % 关闭文件
    fclose(fid);
    disp(['计算结果已写入 CSV 文件: ', output_csv]);
end

function roi_info = load_roi_info(roi_csv, header, delimiter, n)
    if nargin < 4 n=200; end
    if nargin < 3 delimiter = ';';  end
    if nargin < 2 header = true; end
    if nargin < 1 roi_csv=''; end

    roi_info = {};

    if ~isempty(roi_csv)
        fid = fopen(roi_csv, 'r');
        % 如果有表头，跳过
        if header
            fgetl(fid);
        end
        
        tline = fgetl(fid);
        while ischar(tline)
            row = strsplit(tline, delimiter);
            roi_value = str2double(row{1});
            if length(row) < 3 
                row{3} = row{2};
            end
            if length(row) < 4 
                row{4} = row{1};
            end
    
            roi_info{end+1} = {roi_value, row{2}, row{3}, row{4}};
            tline = fgetl(fid);
        end
        fclose(fid);
    else
        for i=1:n
            roi_info{end+1} = {i, ['roi_',i], ['roi_',i], i};
        end
    end 
end

function header = get_header(roi_info, Vox_mm3, SUVr)
    header = {'Subject'};
    for i = 1:numel(roi_info)
        roi_ = roi_info{i};
        roi_name = roi_{2};
        header = [header, roi_name];
        if Vox_mm3
            header = [header, [roi_name, '_Vox_mm3']];
        end
        if SUVr
            header = [header, [roi_name, '_SUVr']];
        end
    end
end
