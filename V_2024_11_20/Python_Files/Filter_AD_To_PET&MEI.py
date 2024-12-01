# 对应每个患者保留一条PET&MRI数据
import os.path
from Move_Trim import Move_Trim
import pandas as pd
from DICOM2NII import Dcm2Nii, Write_log

# 读取数据
data = pd.read_csv('CSV/ADNI2/ADNI2_MRI&PET_ACPC_Y1&Y2.csv')
ADNI = 'ADNI2'
Pre_Path = rf'D:\Matlab\Project\Datasets\AD'

# 移动非缺失数据路径
root_directory = \
    rf"{Pre_Path}\Datasets_Raw\{ADNI}\ADNI"
target_root = \
    rf"{Pre_Path}\Datasets_Filter_From_Raw\{ADNI}\DICOM_PET_MRI"
# DICOM转换路径
DICOM_Root = \
    rf"{Pre_Path}\Datasets_Filter_From_Raw\{ADNI}\DICOM_PET_MRI"
Nii_Root = \
    rf"{Pre_Path}\Datasets_Filter_From_Raw\{ADNI}\DICOM2Nii"

move_miss_file = "Move_Miss_data.csv"
re_path = 'BOTH_MRI_PET.csv'
mi_path = 'MISS_MRI_oR_PET.csv'

Prefix = ''
endswith = ('.dcm', '.v', '.i', '.i.hdr', '.hdr')
moveNocopy = False


def Filter(Data, result_path, miss_path, moveTotargetpath=True):
    # 新增一列用于存储备注
    Data['comment'] = ''

    # 创建一个空的 DataFrame 用于存储结果
    Result = pd.DataFrame(columns=Data.columns)
    Miss_Value = pd.DataFrame(columns=Data.columns)

    subject_id = Data['Subject'].unique()
    # 遍历每个患者
    for subject in subject_id:
        # 过滤该患者的数据
        subject_data = Data[Data['Subject'] == subject]

        # 分离 MRI 和 PET 数据
        mri_data = subject_data[subject_data['Modality'] == 'MRI']
        # 筛选非B1MRI数据
        mri_d_data = mri_data[mri_data['Description'].str.contains('MP', na=False)]
        # TODO
        if not len(mri_d_data):
            mri_d_data = mri_data[~mri_data['Description'].str.contains('B1', na=False)]
            if not len(mri_d_data):
                Miss_Value = pd.concat([Miss_Value, subject_data])
                continue
        mri_data = mri_d_data
        pet_data = subject_data[subject_data['Modality'] == 'PET']

        # 确保只保留一条 MRI 和一条 PET
        if not pet_data.empty and not mri_data.empty:
            matched_mri = mri_data[mri_data['Type'] == 'Processed']
            matched_pet = pet_data[pet_data['Type'] == 'Processed']
            if len(matched_mri):
                Result = pd.concat([Result, matched_mri.head(1)])
                Result.loc[Result.index[-1], 'comment'] = 'Processed'
            else:
                Result = pd.concat([Result, mri_data.head(1)])
            if len(matched_pet):
                Result = pd.concat([Result, matched_pet.head(1)])
                Result.loc[Result.index[-1], 'comment'] = 'Processed'
            else:
                Result = pd.concat([Result, pet_data.head(1)])
        elif pet_data.empty or mri_data.empty:
            # 如果该患者既没有 PET 也没有 MRI，记录到 error_data
            Miss_Value = pd.concat([Miss_Value, subject_data])

    # 重置索引
    Result.reset_index(drop=True, inplace=True)
    Miss_Value.reset_index(drop=True, inplace=True)
    # 打印长度
    re_len = len(Result['Subject'].unique())
    mi_len = len(Miss_Value['Subject'].unique())
    print(f"原始数据 受试者数目: {len(subject_id)}")
    print(f"过滤数据 受试者数目: {re_len}")
    print(f"缺失数据 受试者数目: {mi_len}")
    # 保存结果
    if moveTotargetpath:
        os.makedirs(target_root, exist_ok=True)
        miss_path = os.path.join(os.path.dirname(target_root), miss_path)
        result_path = os.path.join(os.path.dirname(target_root), result_path)
    Result.to_csv(result_path, index=False, encoding='utf-8-sig')
    if not Miss_Value.empty:
        Miss_Value.to_csv(miss_path, index=False, encoding='utf-8-sig')
    print("数据整理完成，已保存至 \n", result_path, "\n", miss_path)
    return os.path.normpath(result_path)


def MRI_Description(MRI_CSV):
    MRI_Data = pd.read_csv(MRI_CSV)
    Description = MRI_Data['Description'].unique()
    print(Description)


if __name__ == '__main__':
    # MRI_CSV = rf'CSV/ADNI2_MRI&PET_ACPC_Y2.csv'
    # MRI_Description(MRI_CSV)

    result_path = Filter(data, re_path, mi_path, moveTotargetpath=True)

    Modality = ['MRI', 'PET']  # 选择需要处理的模态数据
    Move_Trim(Modality, root_directory, target_root, result_path,
              move_miss_file, Prefix, endswith, moveNocopy)

    # # TODO 修改DICOM2NII.py中的exe等文件路径
    Dcm2Nii(DICOM_Root, Nii_Root, Modality, NiiInAll=True,
            del_er=True, only_disp_err=True, verbose_mode=False)
