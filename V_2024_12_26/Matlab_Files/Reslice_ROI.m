% 1. Coregister PET
% 2. ROI
function Reslice_ROI(ref,source,interp,verbose)  
    if nargin < 4 verbose = 0; end
    if nargin < 3 interp = 0; end
    if nargin < 1
        p=spm_select(1,'.nii');
        if size(p,1) <= 0
            return
        end
        f=strtrim(p(1,:));
        ref = deblank(f); %删除路径末尾空白字符
    end
    if nargin < 2 
        p=spm_select(1,'.nii');
        if size(p,1) <= 0
            return
        end
        f=strtrim(p(1,:));
        source = deblank(f);
    end

    matlabbatch{1}.spm.spatial.coreg.write.ref = { ref };
    matlabbatch{1}.spm.spatial.coreg.write.source = { source };
    matlabbatch{1}.spm.spatial.coreg.write.roptions.interp = interp;
    matlabbatch{1}.spm.spatial.coreg.write.roptions.wrap = [0 0 0];
    matlabbatch{1}.spm.spatial.coreg.write.roptions.mask = 0;
    matlabbatch{1}.spm.spatial.coreg.write.roptions.prefix = 'Reslice_';

    if verbose
        spm_jobman('run', matlabbatch); % 执行配准任务
    else
        evalc('spm_jobman(''run'', matlabbatch);');
    end
    disp("Complted !")
end
