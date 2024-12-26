出现任何关于SPM的错误，请先尝试删除SPM的所有预设路径，再重新添加
若不行则，尝试重新安装最新的SPM

配准： AC-PC的MRI TO MNI = rMRI，AC-PC的PET TO 灰质MRI，TO ROI

AC-PC校正：

=======================================================================================
警告: 使用 'state' 设置 RAND 的内部状态，将导致 RAND、RANDI 和 RANDN 使用旧
的随机数生成器。建议不要使用该语法。请参阅替换不提倡使用的 rand 和 randn 语
法，使用 RNG 来替换旧语法。 
> 位置：spm_affreg (第 95 行)
位置: Reorient>auto_reorient (第 82 行)
位置: Reorient (第 18 行)
 
TO
% rand('state',0); % want the results to be consistant.
rng('default') 
rng(0);           % 设置新的随机数生成器种子
=======================================================================================

=======================================================================================
此步骤似乎无影响，可不做，若Reorient失败再尝试这个操作
将spm_cfg.m，spm_cfg_autoreorient.m复制到SPM\config\目录下
已知spm_cfg.m与原SPM目录修改部分如下:
%--------------------------------------------------------------------------
% Spatial
%--------------------------------------------------------------------------
spatial.help    = {'Various spatial and other pre-processing functions.'};
spatial.values  = { spm_cfg_autoreorient spm_cfg_realign spm_cfg_realignunwarp spm_cfg_coreg spm_cfg_preproc8 spm_cfg_norm spm_cfg_smooth };

使用方法：
运行spm_auto_reorient.m,原文件有错误我修改后的：Reorient.m
选择所有需要批量处理的nii文件，可以右击选择全部，点击done.就完成了。
注意校正后的文件直接覆盖原文件，所有最好备份原文件。
还有就是模态单独处理，不要把MRI和PET一起校正，
而是分开，并设置i_type = 'T1'; 为对应模态MRI,PET则是i_type = 'pet'

运行会产生temp.nii，会自动删除，如果没有删除手动删除再运行

如果AC位置偏离太远，模板匹配不上报错：
        There is not enough overlap in the images
        to obtain a solution.
还是需要手动校正到大概位置才可以不然模板匹配不上
但是又很麻烦，所有center_origin=true,先将图像ac设置在图像中心，我这样设置后都能匹配上
=======================================================================================


=======================================================================================
！！！有些PET/fmri图像是4D的,函数File_Split_4DTo3D.m提供方法转换为3D,根据需要选择指定切片
有些PET 扫描是动态的（即在特定时间间隔内多次成像），那么生成的图像数据可以是 4D 的
解释：有些图像是时间序列扫描，每个指定时间扫描一次然后就会有多个时间序列的3D图像：4D,所有切片为3D处理
Main_Fun_Split_4DTo3D.m
可以保留指定切片或者全部切片，volume_to_keep为保留切片的索引，确保其没有超过时间序列索引，为0则保留所有切片
如果输出目录不改且指定了切片会覆盖原文件！！！

出现错误：因为nii是4D，请用Main_Fun_Split_4DTo3D.分割为3D，不会改变本来就是3D的图像，所以随意传入整个目录吧。
Can not use more than one source image.
出错 CN_of_spm_auto_reorient>spm_auto_reorient (第 81 行)
    [M, scal] = spm_affreg(vg,vf,flags);
                ^^^^^^^^^^^^^^^^^^^^^^^
出错 CN_of_spm_auto_reorient (第 130 行)
spm_auto_reorient(p,i_type,p_other)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
=======================================================================================

=======================================================================================
D:\Matlab\R2024b\toolbox\spm12\toolbox\OldNorm   cfg_getfile位于
下面错误是因为spm12的路径没有被完全加入到预设路径，在终端输入spm会自动加入，然后再重新运行。
函数或变量 'cfg_getfile' 无法识别。
出错 spm_select (第 154 行)
    [t, sts] = cfg_getfile(varargin{:});
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
出错 Reorient (第 1 行)
p=spm_select(Inf,'.nii');
^^^^^^^^^^^^^^^^^^^^^^^^^ 
=======================================================================================


=======================================================================================
cat12  roi  xml
【CAT12 ROI tools 转换的csv没有数据 - CSDN App】https://blog.csdn.net/qq_59893890/article/details/143480686?sharetype=blog&shareId=143480686&sharerefer=APP&sharesource=qq_59893890&sharefrom=link
警告: 转义字符 '\M' 无效。有关支持的特殊字符，请参阅 'doc sprintf'。 
> 位置：cat_io_csv>writecsv (第 275 行)
位置: cat_io_csv (第 83 行)
位置: cat_roi_fun>cat_roi_exportSample (第 193 行)
位置: cat_roi_fun (第 45 行)
位置: cat_conf_tools>@(job)cat_roi_fun('exportSample',job) (第 3365 行)
位置: cfg_run_cm (第 26 行)
位置: cfg_util>local_runcj (第 1717 行)
位置: cfg_util (第 972 行)
位置: spm_jobman>fill_run_job (第 469 行)
位置: spm_jobman (第 247 行)
位置: cat12_roi_job (第 15 行)
位置: run (第 112 行)
位置: batch_seg (第 1 行) 

D:\Matlab\R2024b\toolbox\spm12\toolbox\cat12目录下
点击> 位置：cat_io_csv>writecsv (第 275 行)在这个文件crtl+f
找到:M{i}=[M{i} num2str(C{i,j},'%d') opt.delimiter];
替换为
M{i}=[M{i} num2str(strrep(num2str(C{i,j}), '\', '\\'),'%d') opt.delimiter];
原理：C{i,j}是路径是D:\path,但是这里写入文件fprint时\被认为转义字符，替换\为\\
=======================================================================================

=======================================================================================
ROI_<atlas>_<tissue>.csv
<atlas>：表示用于分割大脑区域的解剖学模板或分区方案。
<tissue>：表示组织类型的体积或测量数据。
ROl_aal3_Vgm.csv：基于 AAL3（自动解剖标签3）分区模板生成的灰质体积数据。
ROl_cobra_Vgm.csv 和 ROl_cobra_vwm.csv：基于 COBRA 分区模板的灰质和白质体积数据。
ROl_Ipba40_Vgm.csv 和 ROl_lpba40_vwm.csv：基于 LPBA40（LONI Probabilistic Brain Atlas 40）模板生成的灰质和白质体积数据。
ROl_neuromorphometrics_Vcsf.csv、ROl_neuromorphometrics_Vgm.csv、ROl_neuromorphometrics_Vwm.csv：使用 Neuromorphometrics 模板生成的脑脊液、灰质和白质体积数据。
ROl_suit_Vgm.csv 和 ROl_suit_vwm.csv：基于 SUIT 模板（小脑分割模板）的灰质和白质体积数据，主要用于小脑区域。
ROl_thalamic_nuclei_vgm.csv 和 ROl_thalamus_vgm.csv：基于丘脑核团模板生成的灰质体积数据。
=======================================================================================


=======================================================================================
cat12 segment 生成的文件：
mwp1,mwp2:灰质，白质图像    bias correct 和空间配准
p0:灰质、白质+脑脊液        未配准
wmsub:去除头骨的图像
y_:批量处理时完成了的数据
n_:批量处理时未完成的数据（未完成/被中断，需要重新segment）
=======================================================================================

=======================================================================================
检查配准模板的路径是否错误
错误使用 MATLABbatch system
Job execution failed. The full log of this run can be found in MATLAB command window, starting with the
lines (look for the line showing the exact #job as displayed in this error message)
------------------
Running job #18
------------------
=======================================================================================

=======================================================================================
在 SPM 中，ch2.nii 文件通常指代 MNI152 template 的一种版本，它是在 MNI 标准空间下对一组大脑影像进行配准后的平均图像。
MNI152 是一个标准的大脑模板，广泛应用于神经科学研究中，尤其是在功能和结构影像分析中。
=======================================================================================
