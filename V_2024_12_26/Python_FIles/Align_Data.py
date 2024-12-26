import os
import pandas as pd
from stringcase import uppercase


def check_data(path, info_df, header_keep, m,delimiter=','):
    m = uppercase(m)
    df = pd.read_csv(path, delimiter=delimiter)
    if m == 'MRI':
        df = df.rename(columns={'names': 'Subject'})
    df['Subject'] = df['Subject'].str.extract(r'(\d{3}_S_\d{4})')
    # 4. 提取 PET 和 MRI 数据的 ID，并进行格式化
    df = df.sort_values(by='Subject')

    # # 5. 根据 Subject_ID 关联 info 数据
    # 1. 过滤 info_df 中 Modality 为 'PET' 的行
    info = info_df[info_df['Modality'] == m]
    df = pd.merge(df, info, how='left', left_on='Subject', right_on='Subject')
    df = df[header_keep + [col for col in df.columns if col not in header_keep]]

    if len(df) * 2 != len(info_df):
        print(f'{m}的数据长度{len(df)}，Info的数据长度{len(info)}')
        print('Waring: 检查Failed_Dcm2Nii.csv，是否存在nii转换失败文件，该警告不会影响转换成功的数据')
    return df


def align_data(info_path, pet_path=None, mri_path=None,delimiter=','):
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
    if mri_path:
        mri_df = check_data(mri_path,info_df,header_keep,'MRI',delimiter)
    if pet_path:
        pet_df = check_data(pet_path,info_df,header_keep,'PET',delimiter)

    if mri_path and pet_path:
        null_pet = pet_df[~ pet_df['Subject'].isin(mri_df['Subject'])]
        null_mri = mri_df[~ mri_df['Subject'].isin(pet_df['Subject'])]
        null_df = pd.concat([null_pet, null_mri])
        print("="*100)
        print("There are some non-integrated data:")
        print(null_df['Subject'].values)
        print("="*100)

        pet_df = pet_df[pet_df['Subject'].isin(mri_df['Subject'])]
        mri_df = mri_df[mri_df['Subject'].isin(pet_df['Subject'])]
        pet_df = pet_df.sort_values(by='Subject')
        mri_df = mri_df.sort_values(by='Subject')

        assert len(pet_df) == len(mri_df), f'数据长度不一致：MRI({len(pet_df)}), PET({len(mri_df)})'

    os.makedirs('Result', exist_ok=True)
    if pet_path:
        pet_df.to_csv(f'Result/Align_DATA_PET.csv', index=False)
    if mri_path:
        mri_df.to_csv(f'Result/Align_DATA_MRI.csv', index=False)

    print(f'Completed !')



if __name__ == '__main__':
    # 对齐你的 PET 和 MRI CSV
    # 1. 读取 infoCsv 文件
    info_path = f'ADNI2/idaSearch_12_23_2024.csv'
    pet_path = f'Result/24_12_26/PET_DATA.csv'
    mri_path = f'Result/24_12_26/ROI_aal3_Vgm.csv'

    align_data(info_path, pet_path, mri_path,delimiter=',')