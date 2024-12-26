import os
import re
from pathlib import Path
import pandas as pd

# 正则表达式模式
pdf_pattern = re.compile(r'\d{3}_S_\d{4}')
xml_pattern = re.compile(r'\d{3}_S_\d{4}')

# 获取目录下所有的pdf文件和xml文件
def get_files_in_directory(directory):
    pdf_files = []
    xml_files = []

    # 遍历目录，获取所有pdf和xml文件
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if file.endswith(".pdf"):
            pdf_files.append(file_path)
        elif file.endswith(".xml"):
            xml_files.append(file_path)

    return pdf_files, xml_files

# 从文件名中提取匹配的模式
def extract_pattern(file_path, pattern):
    filename = Path(file_path).stem  # 获取不带扩展名的文件名
    return pattern.findall(filename)
# 删除不匹配的xml文件
def delete_unmatched_xml(pdf_files, xml_files):
    pattern = r'\d{3}_S_\d{4}'
    # 提取所有pdf文件中匹配的模式
    pdf_patterns = set()
    for pdf_file in pdf_files:
        pdf_patterns.update(extract_pattern(pdf_file, pdf_pattern))

    # 遍历xml文件，检查是否存在匹配的模式
    num = 0
    for xml_file in xml_files:
        xml_patterns = extract_pattern(xml_file, xml_pattern)
        if not any(pattern in pdf_patterns for pattern in xml_patterns):
            os.remove(xml_file)
        else:
            dir = os.path.dirname(xml_file)
            name = re.search(pattern, xml_file).group()
            name = 'catROI_'+name + '.xml'
            path = os.path.join(dir, name)
            os.rename(xml_file,path)
            num += 1
    print(f"Residual {num} matched XML files")
# 主函数
def Delete_XML(directory):
    pdf_files, xml_files = get_files_in_directory(directory)

    if not pdf_files:
        print("No PDF files found.")
    if not xml_files:
        print("No XML files found.")

    delete_unmatched_xml(pdf_files, xml_files)

# 读取CSV文件并返回DataFrame
def read_csv(file_path):
    return pd.read_csv(file_path)

# 删除PET数据中，Subject不在MRI数据中出现的行
def filter_pet_by_mri(pet_df, mri_subjects):
    # 只保留PET数据中，Subject列的值在MRI中存在的行
    filtered_pet_df = pet_df[pet_df['Subject'].isin(mri_subjects)]
    return filtered_pet_df

# 保存更新后的PET数据
def save_filtered_pet(filtered_pet_df, output_path):
    filtered_pet_df.to_csv(output_path, index=False)
    print(f"Filtered PET data saved to {output_path}")
# 主函数
def main(mri_file, pet_file, output_file):
    # 读取MRI和PET数据
    mri_df = read_csv(mri_file)
    pet_df = read_csv(pet_file)
    # 获取MRI数据中的Subject列
    mri_df = mri_df.rename(columns={'names': 'Subject'})
    mri_df['Subject'] = mri_df['Subject'].str.extract(r'(\d{3}_S_\d{4})')
    mri_subjects = set(mri_df['Subject'].dropna())  # 去掉空值
    # 筛选PET数据
    filtered_pet_df = filter_pet_by_mri(pet_df, mri_subjects)
    # 保存筛选后的PET数据
    save_filtered_pet(filtered_pet_df, output_file)

# 执行主函数
if __name__ == "__main__":
    # directory = 'D:\Matlab\Project\Datasets\AD\Datasets_Filter_From_Raw\ADNI1\MRI_FILTER'  # 替换为你要操作的目录路径
    # Delete_XML(directory)
    mri_file = 'ROI_aal3_Vgm.csv'  # 替换为MRI文件路径
    pet_file = 'Result/24_12_26/PET_DATA.csv'  # 替换为PET文件路径
    output_file = 'Result/24_12_26/PET_DATA.csv'  # 输出筛选后的PET文件路径

    main(mri_file, pet_file, output_file)
