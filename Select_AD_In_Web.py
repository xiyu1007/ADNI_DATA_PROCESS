# 对应每个患者保留一条PET&MRI数据
import os.path
import pandas as pd

# 读取数据
data = pd.read_csv('idaSearch_11_30_2024.csv')
target_root = '.'

re_path = 'Web_BOTH_MRI_PET.csv'
mi_path = 'Web_MISS_MRI_oR_PET.csv'

Id = 'Subject ID'


def Filter(Data, result_path, miss_path, moveTotargetpath=True):
    # 新增一列用于存储备注
    Data['comment'] = ''

    # 创建一个空的 DataFrame 用于存储结果
    Result = pd.DataFrame(columns=Data.columns)
    Miss_Value = pd.DataFrame(columns=Data.columns)

    subject_id = Data[Id].unique()
    # 遍历每个患者
    for subject in subject_id:
        # 过滤该患者的数据
        subject_data = Data[Data[Id] == subject]

        # 分离 MRI 和 PET 数据
        mri_data = subject_data[subject_data['Modality'] == 'MRI']
        pet_data = subject_data[subject_data['Modality'] == 'PET']

        # 确保只保留一条 MRI 和一条 PET
        if not pet_data.empty and not mri_data.empty:
            matched_mri = mri_data[mri_data['Type'] == 'Processed']
            matched_pet = pet_data[pet_data['Type'] == 'Processed']
            if not matched_mri.empty:
                Result = pd.concat([Result, matched_mri.head(1)])
                Result.loc[Result.index[-1], 'comment'] = 'Processed'
            else:
                Result = pd.concat([Result, mri_data.head(1)])
            if not matched_pet.empty:
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
    re_len = len(Result[Id].unique())
    mi_len = len(Miss_Value[Id].unique())
    print(f"原始数据 受试者数目: {len(subject_id)}")
    print(f"过滤数据 受试者数目: {re_len}")
    print(f"缺数据 受试者数目: {mi_len}")
    # 保存结果
    if moveTotargetpath:
        os.makedirs(target_root, exist_ok=True)
        miss_path = os.path.join(os.path.dirname(target_root), miss_path)
        result_path = os.path.join(os.path.dirname(target_root), result_path)
    Result.to_csv(result_path, index=False, encoding='utf-8-sig')
    if not Miss_Value.empty:
        Miss_Value.to_csv(miss_path, index=False, encoding='utf-8-sig')
    print("数据整理完成，已保存至 \n", result_path, "\n", miss_path)
    return result_path


def Get_ID(result_path):
    # 读取 CSV 文件
    data = pd.read_csv(result_path)

    # 提取 'Subject' 列并去重
    subjects = data['Subject ID'].unique()
    # 将提取的值转换为逗号分隔的字符串
    subjects_string = ','.join(subjects)
    petData = data[data['Modality'] == 'PET']
    # 提取 'Image ID' 列，去重并转为字符串
    petImgid = petData['Image ID'].unique()  # 提取唯一值
    PET_string = ','.join(map(str, petImgid))  # 转为字符串并用逗号拼接
    mriData = data[data['Modality'] == 'MRI']
    mriImgid = mriData['Image ID']
    MRI_string = ','.join(map(str, mriImgid))
    print('PET len: ',len(petImgid),' MRI len: ',len(mriImgid))
    # 将结果写入 TXT 文件
    with open('output.txt', 'w') as f:
        f.write('Subject ID\n')
        f.write(subjects_string)
        f.write('\nMRI Image ID\n')
        f.write(MRI_string)
        f.write('\nPET Image ID\n')
        f.write(PET_string)


    print("Subject 列已写入 output.txt 文件。")


if __name__ == '__main__':
    result_path = Filter(data, re_path, mi_path, moveTotargetpath=True)
    Get_ID(result_path)
