# 对应每个患者保留一条PET&MRI数据
import os.path
import pandas as pd

def Filter(Data, result_path,miss_path,target_root=''):
    info_path = 'Info.txt'
    if target_root != '':
        os.makedirs(target_root, exist_ok=True)
        miss_path = os.path.join(target_root, miss_path)
        result_path = os.path.join(target_root, result_path)
        info_path = os.path.join(target_root, 'Info.txt')
    with open(info_path, 'w'):
        pass

    # 新增一列用于存储备注
    Data['comment'] = ''
    # 创建一个空的 DataFrame 用于存储结果·
    result = pd.DataFrame(columns=Data.columns)
    miss_value = pd.DataFrame(columns=Data.columns)

    subject_id = Data[Id].unique()
    # 遍历每个患者
    for subject in subject_id:
        # 过滤该患者的数据
        subject_data = Data[Data[Id] == subject]

        # 分离 MRI 和 PET 数据
        pet_data = subject_data[subject_data['Modality'] == 'PET']
        mri_data = subject_data[subject_data['Modality'] == 'MRI']
        pet_data = pet_data[pet_data['Type'] == 'Processed']
        mri_data = mri_data[mri_data['Type'] == 'Processed']

        # case 不区分大小写，na缺失值返回false
        # 筛选 'Description' 列包含 'MPR'、'GradWarp'、'B1 Correction' 和 'N3'
        t_data = mri_data[
            mri_data['Description'].str.contains
            (r'(?=.*MPR)(?=.*GradWarp)(?=.*B1 Correction)(?=.*N3)', case=False,na=False)]
        if not t_data.empty:
            # 再次筛选，去掉 'Description' 列包含 'Mask' 的行
            t_data = t_data[~t_data['Description'].str.contains('Mask', case=False, na=False)]
        if t_data.empty:
            mri_data = mri_data[
                mri_data['Description'].str.contains(r'MPR|GradWarp|B1 Correction|N3', case=False, na=False)]
            # 再次筛选，去掉 'Description' 列包含 'Mask' 的行
            mri_data = mri_data[~mri_data['Description'].str.contains('Mask', case=False, na=False)]
        else:
            mri_data = t_data

        pet_data = pet_data[
        pet_data['Description'].str.contains('Coreg, Avg, Standardized Image and Voxel Size', case=False, na=False)]
        if pet_data.empty:
            pet_data = pet_data[~pet_data['Description'].
            str.contains('Coreg, Avg, Std Img and Vox Siz, Uniform', case=False, na=False)]

        # 确保只保留一条 MRI 和一条 PET
        if not pet_data.empty and not mri_data.empty:
            # pet_data = pet_data.copy()
            pet_data['Study Date'] = pd.to_datetime(pet_data['Study Date'], format='%m/%d/%Y')
            pet_data['Study Date'] = pet_data['Study Date'].dt.strftime('%Y-%m-%d')
            mri_data['Study Date'] = pd.to_datetime(mri_data['Study Date'], format='%m/%d/%Y')
            mri_data['Study Date'] = mri_data['Study Date'].dt.strftime('%Y-%m-%d')
            mri_data = mri_data.sort_values(by='Study Date', ascending=False)
            pet_data = pet_data.sort_values(by='Study Date', ascending=False)


            result = pd.concat([result, mri_data.head(1)])

            date = mri_data.head(1)['Study Date'].iloc[0]  # 获取第一个日期
            for index, row in pet_data.iterrows():
                if pd.to_datetime(row['Study Date']).year == pd.to_datetime(date).year:
                    result = pd.concat([result, row.to_frame().T])
                    break
            else:
                result = pd.concat([result, pet_data.head(1)])
                result.loc[result.index[-1], 'comment'] = date
        else:
            miss_value = pd.concat([miss_value, subject_data])

    # 重置索引
    result.reset_index(drop=True, inplace=True)
    miss_value.reset_index(drop=True, inplace=True)

    re_len = len(result[Id].unique())
    mi_len = len(miss_value[Id].unique())
    # 保存结果
    with open(info_path, 'a+',encoding='utf-8-sig') as f:
        f.write(f"原始数据 受试者数目: {len(subject_id)}\n")
        f.write(f"完整数据 受试者数目: {re_len}\n")
        f.write(f"缺失数据 受试者数目: {mi_len}\n")
        group_counts = result['Research Group'].value_counts()
        # 输出每个类别的名称和计数
        for group, count in group_counts.items():
            f.write(f"{group}: {count}\n")
    result.to_csv(result_path, index=False, encoding='utf-8-sig')
    if not miss_value.empty:
        miss_value.to_csv(miss_path, index=False, encoding='utf-8-sig')
    print("数据整理完成，已保存至 \n", result_path, "\n", miss_path)
    return result_path

def Get_Img_ID(result_path,root):
    # 读取 CSV 文件
    data = pd.read_csv(result_path)
    # 提取 'Subject' 列并去重
    subjects = data['Subject ID'].unique()

    # 将提取的值转换为逗号分隔的字符串
    subjects_string = ','.join(subjects)

    petData = data[data['Modality'] == 'PET']
    petImgid = petData['Image ID']
    PET_string = ','.join(map(str, petImgid))  # 转为字符串并用逗号拼接
    mriData = data[data['Modality'] == 'MRI']
    mriImgid = mriData['Image ID']
    MRI_string = ','.join(map(str, mriImgid))

    print('PET IMG LEN: ',len(petImgid),' MRI IMG LEN: ',len(mriImgid))
    # 将结果写入 TXT 文件
    path = os.path.join(root, 'Img_ID.txt')
    with open(path, 'w') as f:
        f.write('Subject ID\n')
        f.write(subjects_string)
        f.write('\nMRI Image ID\n')
        f.write(MRI_string)
        f.write('\nPET Image ID\n')
        f.write(PET_string)
        f.write('\nPET AND MRI Image ID\n')
        f.write(PET_string)
        f.write(',')
        f.write(MRI_string)
        f.write('\n')
    print(f"Img ID 写入 {path} 文件")


if __name__ == '__main__':
    # 读取数据
    data = pd.read_csv('ADNI2/idaSearch_12_01_2024.csv')
    Id = 'Subject ID'

    target_root = 'ADNI2/output' # 保存的目录，输出的文件保存目录，可用为空
    re_path = 'Web_BOTH_MRI_PET.csv' # 输出的结果文件名
    mi_path = 'Web_MISS_MRI_oR_PET.csv'

    result_csv= Filter(data,re_path,mi_path,target_root)
    Get_Img_ID(result_csv,target_root)
