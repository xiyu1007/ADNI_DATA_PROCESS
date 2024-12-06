import os
import numpy as np
import SimpleITK as sitk
import csv

import pandas as pd
from tqdm import tqdm

def load_roi_info(roi_csv, header=False, delimiter=' '):
    """
    从CSV文件加载ROI信息，返回一个字典，键为ROI的值，值为元组(ROIid, ROIabbr, ROIname)。
    """
    roi_info = {}
    with open(roi_csv, mode='r') as file:
        reader = csv.reader(file, delimiter=delimiter)
        if header:
            next(reader)  # 跳过表头
        for row in reader:
            roi_value = int(row[0])
            if len(row) <= 2:
                row.append(row[0])
            roi_info[roi_value] = (roi_value, row[1], row[2])
    return roi_info

def get_header(roi_info,Vox_mm3,SUVr):
    # 写入CSV头部
    header = ['Subject']
    for v in roi_info.keys():
        header.append(roi_info[v][1])
        if Vox_mm3:
            header.append(roi_info[v][1] + '_Vox_mm3')
        if SUVr:
            header.append(roi_info[v][1] + '_SUVr')
    return header

def get_pet_data(mask_path, nii_dir, output_csv, startswith='r', cerebellar=False, Vox_mm3=True, roi_info=None, subject_info=None, SUVr=False):
    ID = 'Subject ID'
    Injected_dose = 185  # MBq，FDG-PET Reference ADNI
    cerebellar_ID = []  # 95~120
    ce_suv = 1
    weight = -1
    s_info = None
    if SUVr:
        if subject_info:
            s_info = pd.read_csv(subject_info)
            s_info = s_info[s_info['Modality'] == 'PET']
            # 计算SUVr的值以小脑标准化，AAL3图谱小脑区为：
            cerebellar_ID = np.arange(95, 121)  # 95~120
        else:
            print("Calculating the SUVr must input the subject_info(Weight) parameter")
            return

    if roi_info is None:
        roi_info = {}

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        write_header = False
        # 获取 .nii 或 .nii.gz 文件
        nii_files = [f for f in os.listdir(nii_dir) if
                     (f.endswith('.nii') or f.endswith('.nii.gz')) and f.startswith(startswith)]

        for nii_filename in tqdm(nii_files, desc="Processing NIfTI Files", unit="file"):
            nii_path = os.path.join(nii_dir, nii_filename)
            nii = sitk.ReadImage(nii_path)
            nii_array = sitk.GetArrayFromImage(nii)

            # 读取mask文件，获取唯一值
            mask = sitk.ReadImage(mask_path)
            mask_array = sitk.GetArrayFromImage(mask)
            unique_values = np.unique(mask_array)[np.unique(mask_array) != 0]  # 排除0

            # 如果没有提供roi_info，创建默认的ROI信息
            if not write_header:
                # 检查ROI长度与MASK长度是否一致
                if len(unique_values) != len(roi_info):
                    print(f"\nROI_INFO长度({len(roi_info)})"
                          f"ROI.nii({len(unique_values)})不一致,导致对应roi为0")
                header = get_header(roi_info,Vox_mm3,SUVr)
                writer.writerow(header)
                write_header = True

            if SUVr:
                sid,_ = os.path.splitext(nii_filename)
                sid = sid[len(prefix):]
                # sid = sid.removeprefix(prefix)
                weight_ = s_info[s_info[ID] == sid]['Weight']
                if len(weight_) >0:
                    weight = float(weight_.iloc[0]) * 1000
                else:
                    print(f'{sid} have not weight, SUVr May be 0')
                sum_ce = 0
                for ci in cerebellar_ID:
                    # 获取template中等于当前值的所有索引
                    indices = np.argwhere(mask_array == ci)
                    # ce_vox_num = len(indices)
                    ce_vox_in = nii_array[tuple(indices.T)]  # 转置索引，使其符合np的索引格式
                    sum_ce += np.sum(ce_vox_in)
                ce_suv = sum_ce/(Injected_dose*weight)

            average_values = []
            for value in roi_info.keys():
                avg_intensity = 0
                vox_mm3 = 0
                roi_suvr = 0
                if (value not in unique_values) or (value in cerebellar_ID and not cerebellar):
                    pass
                else: # value in unique_values
                    # 获取template中等于当前值的所有索引
                    indices = np.argwhere(mask_array == value)
                    intensity = nii_array[tuple(indices.T)]  # 转置索引，使其符合np的索引格式
                    avg_intensity = np.mean(intensity)
                    sum_intensity = np.sum(intensity)

                    vox_mm3 = len(indices)
                    roi_suv = sum_intensity/(Injected_dose*weight) if weight != -1 else 0
                    roi_suvr = roi_suv/ce_suv

                average_values.append(str(avg_intensity))
                if Vox_mm3:
                    average_values.append(str(vox_mm3))
                if SUVr:
                    average_values.append(str(roi_suvr))

            writer.writerow([nii_filename] + average_values)
        print(f"计算结果已写入 CSV 文件: {output_csv}")


if __name__ == '__main__':
    # 使用示例
    ROI = 'Template/AAL3v1_1mm.nii' #ROI的路径
    PET = 'PET'  # 配准后的PET目录
    prefix = 'r'  # 与配准后的pet文件格式对应: r受试者id.nii，r表示处理r开头的数据
    Subject_Info_path = 'ADNI2/idaSearch_12_01_2024.csv'
    roi_csv = 'Template/AAL3v1_1mm.nii.txt'  # ROI信息文件路径
    ROI_INFO = load_roi_info(roi_csv, header=False, delimiter=' ')
    # roi_csv = 'Template/AAL3v1_1mm.csv'  # ROI信息文件路径
    # ROI_INFO = load_roi_info(roi_csv, header=True, delimiter=';')

    output_csv = 'AAL3v1_1mm_PET_.csv'  # 输出CSV文件路径


    # 除intensity之外，是否(0)计算小脑区域的值，计算ROI体积，SUVr(SUVr必须传入包含患者体重的Subject_info)
    get_pet_data(ROI, PET, output_csv, prefix, cerebellar=True,
                 Vox_mm3=True, roi_info=ROI_INFO, subject_info=Subject_Info_path, SUVr=True)

