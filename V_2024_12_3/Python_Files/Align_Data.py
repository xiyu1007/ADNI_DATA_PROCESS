import pandas as pd

delimiter = ','
ROI = 'AAL3v1'
ADNI = 'ADNI1'
# 1. 读取 infoCsv 文件
info_path = f'CSV/{ADNI}/BOTH_MRI_PET.csv'
pet_path = f'CSV/{ADNI}/PET_{ROI}.csv'
mri_path = f'CSV/{ADNI}/MRI_{ROI}_Vgm.csv'
MTS = f'CSV/{ADNI}/idaSearch_11_10_2024.csv'

# 读取 MMSE 文件
MMSE_header = ['Subject ID', 'MMSE Total Score', 'Global CDR']
MMSE_df = pd.read_csv(MTS, delimiter=delimiter, usecols=MMSE_header)
MMSE_df.rename(columns={
    'Subject ID': 'Subject',
    'MMSE Total Score': 'MTS',
    'Global CDR': 'CDR'
}, inplace=True)

# 读取 info 文件
info_df = pd.read_csv(info_path, delimiter=delimiter)

# 检查数据长度是否一致
# 去重并保留首次出现的 Subject 记录
MMSE_df = MMSE_df.drop_duplicates(subset='Subject', keep='first')
if len(MMSE_df) * 2 != len(info_df):
    print(f'数据长度不一致：info({len(info_df)}), CDR({len(MMSE_df)})')
# 如果 info_df 中已经存在 'MTS' 或 'CDR' 列，则从 MMSE_df 中删除这些列
for col in ['MMSE Total Score', 'Global CDR']:
    if col in info_df.columns:
        info_df.drop(columns=col, inplace=True)
# 合并两个 DataFrame（只合并不冲突的列）
info_df = pd.merge(info_df, MMSE_df, how='left', on='Subject')

header_cols = ['Subject', 'Group', 'Sex', 'Age', 'MTS', 'CDR', 'Modality']
info_df = info_df[header_cols]

# 2. 读取 PET 数据
pet_df = pd.read_csv(pet_path,delimiter=delimiter)
# 3. 读取 MRI 数据
mri_df = pd.read_csv(mri_path,delimiter=delimiter)

assert len(pet_df) == len(mri_df),f'数据长度不一致：MRI({len(pet_df)}), PET({len(mri_df)})'
if len(pet_df)*2 != len(info_df):
    print('Waring: 检查Failed_Dcm2Nii.csv，是否存在nii转换失败文件，该警告不会影响转换成功的数据')

# 4. 提取 PET 和 MRI 数据的 ID，并进行格式化
pet_df['Subject'] = pet_df['NIfI File'].str.replace('^r', '', regex=True, n=1).str.replace('.nii$', '', regex=True)
pet_df.drop(pet_df.columns[0], axis=1, inplace=True)  # 去掉第一列
pet_df = pet_df.sort_values(by='Subject')

mri_df['Subject'] = mri_df['names'].apply(lambda x: x.split('\\')[-1]).str.replace('^r', '', regex=True, n=1)
mri_df.drop(mri_df.columns[0], axis=1, inplace=True)  # 去掉第一列
mri_df = mri_df.sort_values(by='Subject')

# # 5. 根据 Subject_ID 关联 info 数据
# 1. 过滤 info_df 中 Modality 为 'PET' 的行
info_pet = info_df[info_df['Modality'] == 'PET']
pet_df = pd.merge(pet_df, info_pet, how='left', left_on='Subject', right_on='Subject')
pet_df = pet_df[header_cols + [col for col in pet_df.columns if col not in header_cols]]

info_mri = info_df[info_df['Modality'] == 'MRI']
mri_df = pd.merge(mri_df, info_mri, how='left', left_on='Subject', right_on='Subject')
mri_df = mri_df[header_cols + [col for col in mri_df.columns if col not in header_cols]]

pet_df.to_csv(f'CSV/Align_{ROI}_Data_PET.csv', index=False)
mri_df.to_csv(f'CSV/Align_{ROI}_Data_MRI.csv', index=False)

print(f'数据已对齐: Align_{ROI}_Data_PET.csv,\tAlign_{ROI}_Data_MRI.csv')



