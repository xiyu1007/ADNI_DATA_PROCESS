function normalise_job(def,source,interp,outputPrefix,verbose)
    bb = [-100 -130 -90; % 左 侧右 下
        100 90 105]; % Bounding box
    % bb = [-78 -112  -70;
    %         78   76   85]; % Bounding box

    vox = [1 1 1]; % vox size
    if nargin < 3
        interp = 1;
    end
    if nargin < 4 || isempty(outputPrefix)
        outputPrefix = 'w';
    end
    if nargin < 5
        verbose = true;
    end
    matlabbatch{1}.spm.spatial.normalise.write.subj.def = {def};
    matlabbatch{1}.spm.spatial.normalise.write.subj.resample = {source};
    matlabbatch{1}.spm.spatial.normalise.write.woptions.bb = bb;
    matlabbatch{1}.spm.spatial.normalise.write.woptions.vox = vox;
    matlabbatch{1}.spm.spatial.normalise.write.woptions.interp = interp;
    matlabbatch{1}.spm.spatial.normalise.write.woptions.prefix = outputPrefix;

    if verbose
        spm_jobman('run', matlabbatch); % 执行配准任务
    else
        evalc('spm_jobman(''run'', matlabbatch);');
    end
end