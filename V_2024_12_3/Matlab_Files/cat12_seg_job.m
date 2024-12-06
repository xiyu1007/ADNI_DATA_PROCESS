%-----------------------------------------------------------------------
% Job saved on 04-Nov-2024 08:59:39 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7771)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
function cat12_seg_job(inputFiles,nproc,mask)
    % run_spm_job.m
    % 此文件用于调用和运行 SPM 批处理任务
    % 输入参数：
    %   inputFiles: N x 1 cell array of file paths to be processed
    if nargin<3
        mask = fullfile(spm('dir'),'toolbox\cat12\templates_MNI152NLin2009cAsym\aal3.nii');
        mask = [mask,',1'];
    end

    % 初始化批处理变量
    matlabbatch = {};
    
    % 设置数据输入
    matlabbatch{1}.spm.tools.cat.estwrite.data = inputFiles;  % 使用传入的文件路径
    matlabbatch{1}.spm.tools.cat.estwrite.data_wmh = {''};
    matlabbatch{1}.spm.tools.cat.estwrite.nproc = nproc;
    matlabbatch{1}.spm.tools.cat.estwrite.useprior = '';
    matlabbatch{1}.spm.tools.cat.estwrite.opts.tpm = {'D:\Matlab\R2024b\toolbox\spm12\tpm\TPM.nii'};
    matlabbatch{1}.spm.tools.cat.estwrite.opts.affreg = 'mni';
    matlabbatch{1}.spm.tools.cat.estwrite.opts.biasacc = 0.5;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.restypes.optimal = [1 0.3];
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.setCOM = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.APP = 1070;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.affmod = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.LASstr = 0.5;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.LASmyostr = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.gcutstr = 2;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.WMHC = 2;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.registration.shooting.shootingtpm = {'D:\Matlab\R2024b\toolbox\spm12\toolbox\cat12\templates_MNI152NLin2009cAsym\Template_0_GS.nii'};
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.registration.shooting.regstr = 0.5;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.vox = 1.5;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.bb = 12;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.SRP = 22;
    matlabbatch{1}.spm.tools.cat.estwrite.extopts.ignoreErrors = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.BIDS.BIDSno = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.surface = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.surf_measures = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.neuromorphometrics = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.lpba40 = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.cobra = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.hammers = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.thalamus = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.thalamic_nuclei = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.suit = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.ibsr = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ROImenu.atlases.ownatlas = mask;
    matlabbatch{1}.spm.tools.cat.estwrite.output.GM.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.GM.mod = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.GM.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.WM.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.WM.mod = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.WM.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.CSF.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.CSF.warped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.CSF.mod = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.CSF.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ct.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ct.warped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.ct.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.pp.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.pp.warped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.pp.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.WMH.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.WMH.warped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.WMH.mod = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.WMH.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.SL.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.SL.warped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.SL.mod = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.SL.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.TPMC.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.TPMC.warped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.TPMC.mod = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.TPMC.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.atlas.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.label.native = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.label.warped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.label.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.labelnative = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.bias.warped = 1;
    matlabbatch{1}.spm.tools.cat.estwrite.output.las.native = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.las.warped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.las.dartel = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.jacobianwarped = 0;
    matlabbatch{1}.spm.tools.cat.estwrite.output.warps = [1 0];
    matlabbatch{1}.spm.tools.cat.estwrite.output.rmat = 0;

    % 调用 spm_run 执行批处理作业
    spm('defaults', 'FMRI');  % 确保 SPM 默认设置已初始化
    spm_jobman('run', matlabbatch);  % 执行批处理任务
end
