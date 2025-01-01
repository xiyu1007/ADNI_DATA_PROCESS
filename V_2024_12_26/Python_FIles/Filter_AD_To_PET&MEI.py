from Move_Trim import Move_Trim
from DICOM2NII import Dcm2Nii

# 读取数据
csv_path = 'ADNI1/ADNI1_354_12_23_2024.csv'
#TODO 修改DICOM2NII.py中的exe等文件路径
#TODO 根据csv修改为Subject ID或Subject
ID = 'Subject'

ADNI = 'ADNI1'
Pre_Path = rf'D:\_DATASETS' # 可自定义
# 解压后的数据根目录为ADNI
root_directory = \
    rf"E:\DATASETS\ADNI\RAW\ADNI1\ADNI"
target_root = \
    rf"{Pre_Path}\Filter\{ADNI}\DICOM_PET_MRI"
# DICOM转换路径
DICOM_Root = \
    rf"{Pre_Path}\Filter\{ADNI}\DICOM_PET_MRI"
Nii_Root = \
    rf"{Pre_Path}\Filter\{ADNI}\DICOM2Nii"

# 移动数据而不是复制
moveNocopy = False

move_miss_path = "Move_Miss_data.csv"
re_path = 'BOTH_MRI_PET.csv'
mi_path = 'MISS_MRI_oR_PET.csv'

endswith = ('.dcm', '.v', '.i', '.i.hdr', '.hdr','.nii')

if __name__ == '__main__':
    Modality = ['MRI','PET']  # 选择需要处理的模态数据
    Move_Trim(ID,Modality, root_directory, target_root, csv_path,
              move_miss_path, endswith, moveNocopy)

    # # TODO 修改DICOM2NII.py中的exe等文件路径
    # niiCopy 如果存在nii文件则直接复制而不是转换
    Dcm2Nii(DICOM_Root, Nii_Root, Modality, niiCopy=True,
            del_er=False, only_disp_err=True, verbose_mode=False,NiiInAll=True,)
