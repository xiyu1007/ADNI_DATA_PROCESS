import csv
import glob
import os
import shutil
import subprocess

from tqdm import tqdm

# TODO
# 指定 dcm2niix.exe 的路径
# 终端D:\DICOM2NII\MRIcron\Resources\dcm2niix.exe -h查看参数
dcm2niix_path = r'D:\DICOM2NII\MRIcron\Resources\dcm2niix.exe'  # 请根据实际路径修改

ADNI = 'ADNI1'
Pre_Path = rf'D:\Matlab\Project\Datasets\AD' # 可自定义
# DICOM转换路径
DICOM_Root = \
    rf"{Pre_Path}\Datasets_Filter_From_Raw\{ADNI}\DICOM_PET_MRI"
Nii_Root = \
    rf"{Pre_Path}\Datasets_Filter_From_Raw\{ADNI}\DICOM2Nii"
Modality = ['MRI', 'PET']

# 输出 NIfTI 文件夹
filename_format = '%i'  # 文件名格式
bids_sidecar = 'y'  # 生成 BIDS 辅助文件 json
philips_scaling = 'y'  # 启用 Philips 精确浮点缩放
bids_anonymize = 'n'  # BIDS 辅助文件的匿名处理（y: 是，n: 否）
include_patient_details = 'n'  # 生成包含私人患者详细信息  txt
write_behavior = '1'  # 处理名称冲突的写入行为（0=跳过重复项，1=覆盖，2=添加后缀）
zip2gz = 'n'


def Dcm2Nii(DICOM_Root, Nii_Root, Modality,niiCopy=True,del_er=True, verbose_mode= False, only_disp_err=True,NiiInAll=True):
    error_warnings_log = os.path.join(os.path.dirname(Nii_Root), "Error_log_Dcm2Nii.txt")
    with open(error_warnings_log, 'w'):
        pass
    # 存储转换失败的记录
    failed_conversions = []
    # 遍历root目录下的MRI和PET文件夹
    for modality in Modality:
        modality_path = os.path.join(DICOM_Root, modality)
        for patient_folder in tqdm(os.listdir(modality_path), desc=f"{modality} Dicom To Nii ...", unit="file"):
            input_root = os.path.join(modality_path, patient_folder)
            # 检查是否为目录
            if os.path.isdir(input_root):
                # 设置输出目录路径，与 input_directory 对应
                if NiiInAll:
                    output_root = os.path.join(Nii_Root, modality)
                else:
                    output_root = os.path.join(Nii_Root, modality, patient_folder)
                os.makedirs(output_root, exist_ok=True)  # 如果不存在，则创建输出目录
                ex_Nii= glob.glob(os.path.join(input_root, "*.nii"))
                if len(ex_Nii) > 0 and niiCopy:
                    for fn in os.listdir(input_root):
                        src_path = os.path.join(input_root, fn)  # 源路径
                        dst_path = os.path.join(output_root, str(patient_folder)+'.nii')  # 目标路径
                        if os.path.exists(dst_path):
                            base, ext = os.path.splitext(dst_path)
                            counter = 1
                            # 如果目标文件已存在，生成新的文件名
                            while os.path.exists(dst_path):
                                dst_path = f"{base}_{counter}{ext}"
                                counter += 1
                        shutil.copy(src_path, dst_path)
                    continue
                # 构造 dcm2niix 命令
                command = [
                    dcm2niix_path,  # dcm2niix 可执行文件路径
                    '-f', filename_format,  # 文件名格式
                    '-o', output_root,  # 输出目录
                    '-p', philips_scaling,  # Philips 精确浮点缩放
                    '-t', include_patient_details,  # 包含私人患者详细信息
                    '-b', bids_sidecar,  # 生成 BIDS 辅助文件
                    '-ba', bids_anonymize,  # 对 BIDS 辅助文件进行匿名处理
                    '-w', write_behavior,  # 处理名称冲突的写入行为
                    '-z', zip2gz,
                    input_root  # 输入文件夹
                ]
                try:
                    # 调用 dcm2niix 进行转换
                    # subprocess.run(command)
                    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if not only_disp_err:
                        print('\n'+"=" * 100)
                        if verbose_mode:
                            print(f"\n转换成功:{str(patient_folder)}--{modality}\t", result.stdout.decode())
                        else:
                            print(
                                f"\nConverted DICOM files {str(patient_folder)} to NIfTI format.")
                except subprocess.CalledProcessError as e:
                    print('\n'+"=" * 100)
                    print(f"存在错误/警告:{str(patient_folder)}--{modality}\n", e.stderr.decode())  # 输出错误信息
                    # 如果需要，可以检查并记录警告信息
                    err = e.stderr.decode().strip()
                    out = e.stdout.decode().strip()
                    if err or out:
                        # 记录错误警告信息
                        with open(error_warnings_log, 'a') as log_file:
                            log_file.write(f"{patient_folder}--{modality}:\n{out}\n{err}\n\n")
                    failed_conversions.append((str(patient_folder), str(modality)))
    print('\n'+"=" * 100)
    if failed_conversions and del_er:
        for patient_folder, modality in failed_conversions:
            # 删除 MRI 和 PET 下对应的 patient_folder
            for m in Modality:
                if NiiInAll:
                    Endswith = ['.nii', '.json', '.txt']
                    sub = ''
                    for endswith in Endswith:
                        nii_to_delete = os.path.join(Nii_Root, m, patient_folder + endswith)
                        if os.path.exists(nii_to_delete):
                            if NiiInAll:
                                os.remove(nii_to_delete)  # 删除指定文件
                else:
                    nii_to_delete = os.path.join(Nii_Root, m, sub)
                    if os.path.exists(nii_to_delete):
                        shutil.rmtree(nii_to_delete)  # 删除文件夹及其内容
                print(f"已删除异常患者文件: {m}--{patient_folder}")
    Write_log(failed_conversions)
    return failed_conversions


def Write_log(failed_conversions):
    Failed_Dcm2Nii = os.path.join(os.path.dirname(Nii_Root), "Failed_Dcm2Nii.csv")
    if failed_conversions:
        with open(Failed_Dcm2Nii, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Subject', 'Modality'])  # 写入标题
            for folder, modality in failed_conversions:
                writer.writerow([folder, modality])  # 写入失败的记录
    print(f"记录了 {len(failed_conversions)} 个异常的转换到\n {Failed_Dcm2Nii}.")


def Single_Dicom2Nii():
    # 单条
    # 存储dicom文件的目录
    DICOM_Dir = \
        rf"{Pre_Path}\Datasets_Filter_From_Raw\{ADNI}\DICOM_PET_MRI\MRI\137_S_0686"
    Nii_Dir = rf"."

    # 构造 dcm2niix 命令
    command = [
        dcm2niix_path,  # dcm2niix 可执行文件路径
        '-f', filename_format,  # 文件名格式
        '-o', Nii_Dir,  # 输出目录
        '-p', philips_scaling,  # Philips 精确浮点缩放
        '-t', include_patient_details,  # 包含私人患者详细信息
        '-b', bids_sidecar,  # 生成 BIDS 辅助文件
        '-ba', bids_anonymize,  # 对 BIDS 辅助文件进行匿名处理
        '-w', write_behavior,  # 处理名称冲突的写入行为
        '-z', zip2gz,
        '-d', 'myInstanceNumberOrderIsNotSpatial',  # 将 -D 和参数分开
        DICOM_Dir  # 输入文件夹
    ]
    try:
        # 调用 dcm2niix 进行转换
        # subprocess.run(command)
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("=" * 100)
        print(result)
        print(f"Converted DICOM files {str(DICOM_Dir)} to NIfTI format.")
    except subprocess.CalledProcessError as e:
        print("=" * 100)
        err = e.stderr.decode().strip()
        out = e.stdout.decode().strip()
        print(f"存在错误/警告:{str(DICOM_Dir)}\n{err}\n{out}\n")  # 输出错误信息


if __name__ == '__main__':
    print(f"Converting DICOM files to NIfTI format...")
    Dcm2Nii(DICOM_Root, Nii_Root, Modality, niiCopy=True,
            del_er=True, only_disp_err=True, verbose_mode=True,NiiInAll=True)
    #在函数中修改单个转换的目录
    # Single_Dicom2Nii()
    print(f"Converting Over!")
