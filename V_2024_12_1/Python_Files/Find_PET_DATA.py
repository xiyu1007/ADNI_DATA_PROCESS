import pandas as pd
import numpy as np

# 假设 Data 是包含所有数据的 DataFrame
# 假设 PET_DATA 是包含 PET 数据的 DataFrame

# 读取数据
Data = pd.read_csv('ADNI1/output/idaSearch_12_01_2024.csv')
PROCESSED_PET_DATA = pd.read_csv('CSV/UCBERKELEY_AMY_6MM_30Nov2024.csv')
Result = pd.DataFrame(columns=Data.columns)
PET_Result = pd.DataFrame(columns=PROCESSED_PET_DATA.columns)

subject_id = Data['Subject ID'].unique()
# 遍历每个患者
for subject in subject_id:
    # 获取该患者的 PET 信息和对应的 PET_DATA 数据
    pet = Data[Data['Modality'] == 'PET']
    pet_info = Data[Data['Subject ID'] == subject]

    corr_pet = PROCESSED_PET_DATA[PROCESSED_PET_DATA['PTID'] == subject]
    if not corr_pet.empty and not pet_info.empty:
        # 将 'Study Date' 列转换为 datetime 类型
        pet_info['Study Date'] = pd.to_datetime(pet_info['Study Date'], format='%m/%d/%Y')
        # 将 'Study Date' 格式化为 'YYYY-MM-DD' 格式
        pet_info['Study Date'] = pet_info['Study Date'].dt.strftime('%Y-%m-%d')

        pet_info = pet_info.sort_values(by='Study Date')
        corr_pet =  corr_pet.sort_values(by='SCANDATE')
        Result = pd.concat([Result, pet_info.head(1)])
        Result.loc[Result.index[-1], 'comment'] = corr_pet['SCANDATE'](1)
        most_close_scan_date = corr_pet['SCANDATE'].iloc[0]
        # 将最接近的 SCANDATE 对应的值添加到 Result 中
        Result.loc[Result.index[-1], 'comment'] = most_close_scan_date
    else:
        print('No pet data')
    # print(Result)
    break
