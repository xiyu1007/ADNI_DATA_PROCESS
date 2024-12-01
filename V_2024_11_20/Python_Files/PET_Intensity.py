import os
import warnings
import numpy as np
import SimpleITK as sitk
import csv
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


def calculate_average_values(mask_dir, nii_dir, output_csv, Prefix, roi_info=None, startswith=''):
    """
    计算NIfTI文件在给定mask下的平均体素值，并写入CSV文件。
    """
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

            mask_path = os.path.join(mask_dir, f'{Prefix}{nii_filename}')
            if not os.path.exists(mask_path):
                print(f"\nMask file not found: {mask_path}")
                continue
            # 读取mask文件，获取唯一值
            mask_nii = sitk.ReadImage(mask_path)
            mask_array = sitk.GetArrayFromImage(mask_nii)
            unique_values = np.unique(mask_array)[np.unique(mask_array) != 0]  # 排除0值

            # 如果没有提供roi_info，创建默认的ROI信息
            if not roi_info:
                roi_info = {}
                for v in range(1,max(unique_values)+1):
                    roi_info[v] = (v,f"ROI_{v}", f"ROI_{v}")
            # 写入CSV头部
            header = ['NIfI File'] + [roi_info[v][1] for v in roi_info.keys()]
            if not write_header:
                # 检查ROI长度与MASK长度是否一致
                if len(unique_values) != len(roi_info):
                    print(f"\nroi_info长度{len(roi_info)}"
                          f"和MASK{len(unique_values)}不一致,导致对应roi为0")
                writer.writerow(header)
                write_header = True

            average_values = []
            for value in roi_info.keys():
                if value in unique_values:
                    # 获取template中等于当前值的所有索引
                    indices = np.argwhere(mask_array == value)
                    # print('value:',value,' Vox num: ', len(indices))
                    voxel_values = nii_array[tuple(indices.T)]  # 转置索引，使其符合np的索引格式
                    avg_value = np.mean(voxel_values)
                    # 将计算的平均值转换为字符串并添加到列表中
                    average_values.append(str(avg_value))
                else:
                    average_values.append(str(0))
            writer.writerow([nii_filename] + average_values)
        print(f"计算结果已写入 CSV 文件: {output_csv}")


# 使用示例
ROI = r'testPET_ROI'  # 配准后的ROI文件目录！
PET = r'testPET'  # 配准后的PET目录

roi_csv = 'temp/AAL3v1.nii.txt'  # ROI信息文件路径
ROI_INFO = load_roi_info(roi_csv, header=False, delimiter=' ')
# roi_csv = 'AAL3v1_1mm.csv'  # ROI信息文件路径
# ROI_INFO = load_roi_info(roi_csv, header=True, delimiter=';')

output_csv = 'PET_AAL3v1_1mm.csv'  # 输出CSV文件路径
Prefix = 'AAL3v1_1mm_'  # ROI的名称，与ROI文件名对应，并加一个_

# 加载ROI信息
# 计算NIfTI文件的平均值并写入CSV
calculate_average_values(ROI, PET, output_csv, Prefix, ROI_INFO, startswith='r')
