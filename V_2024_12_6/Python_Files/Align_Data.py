import os

import pandas as pd


def align_data(info_path, pet_path, mri_path,delimiter=','):
    # 读取 info 文件
    info_df = pd.read_csv(info_path, delimiter=delimiter)
    # 定义列名的映射关系（将原列名映射为简写）
    column_mapping = {
        'Subject ID': 'Subject',
        'Sex': 'Sex',
        'Weight': 'Weight',
        'Research Group': 'Group',
        'APOE A1': 'APA1',
        'APOE A2': 'APA2',
        'Age': 'Age',
        'Global CDR': 'CDR',
        'NPI-Q Total Score': 'NPI_Q',
        'MMSE Total Score': 'MMSE',
        'GDSCALE Total Score': 'GDS',
        'FAQ Total Score': 'FAQ',
        'Modality': 'Modality'
    }
    # 使用 rename 方法进行列名替换
    info_df = info_df.rename(columns=column_mapping)
    header_keep = ['Subject', 'Group', 'Modality', 'Weight', 'Sex', 'Age', 'CDR', 'NPI_Q', 'MMSE', 'GDS', 'FAQ', 'APA1',
                   'APA2']
    info_df = info_df[header_keep]

    # 2. 读取 PET 数据
    pet_df = pd.read_csv(pet_path, delimiter=delimiter)
    # 3. 读取 MRI 数据
    mri_df = pd.read_csv(mri_path, delimiter=delimiter)
    mri_df = mri_df.rename(columns={'names': 'Subject'})
    mri_df['Subject'] = mri_df['Subject'].str.extract(r'(\d{3}_S_\d{4})')

    assert len(pet_df) == len(mri_df), f'数据长度不一致：MRI({len(pet_df)}), PET({len(mri_df)})'

    if len(pet_df) * 2 != len(info_df):
        print(f'存在的数据长度{len(pet_df) * 2}，Info的数据长度{len(info_df)}')
        print('Waring: 检查Failed_Dcm2Nii.csv，是否存在nii转换失败文件，该警告不会影响转换成功的数据')

    # 4. 提取 PET 和 MRI 数据的 ID，并进行格式化
    pet_df = pet_df.sort_values(by='Subject')
    mri_df = mri_df.sort_values(by='Subject')

    # # 5. 根据 Subject_ID 关联 info 数据
    # 1. 过滤 info_df 中 Modality 为 'PET' 的行
    info_pet = info_df[info_df['Modality'] == 'PET']
    pet_df = pd.merge(pet_df, info_pet, how='left', left_on='Subject', right_on='Subject')
    pet_df = pet_df[header_keep + [col for col in pet_df.columns if col not in header_keep]]

    info_mri = info_df[info_df['Modality'] == 'MRI']
    mri_df = pd.merge(mri_df, info_mri, how='left', left_on='Subject', right_on='Subject')
    mri_df = mri_df[header_keep + [col for col in mri_df.columns if col not in header_keep]]

    os.makedirs('Result', exist_ok=True)
    pet_df.to_csv(f'Result/Align_DATA_PET.csv', index=False)
    mri_df.to_csv(f'Result/Align_DATA_MRI.csv', index=False)

    print(f'数据已对齐')



if __name__ == '__main__':
    # 1. 读取 infoCsv 文件
    info_path = f'ADNI1/output/Web_BOTH_MRI_PET.csv'
    pet_path = f'PET_DATA.csv'
    mri_path = f'ROI_aal3_Vgm.csv'

    align_data(info_path, pet_path, mri_path,delimiter=',')