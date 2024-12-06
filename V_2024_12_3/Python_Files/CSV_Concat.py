# 合并文件（追加）
import pandas as pd

# 读取两个CSV文件
df1 = pd.read_csv('Cohort_1_MRI_Images_30Nov2024.csv')
df2 = pd.read_csv('Cohort_1_PET_Images_30Nov2024.csv')

# 将df1追加到df2的末尾
df_combined = pd.concat([df1,df2], ignore_index=True)
# 将合并后的数据写入新的CSV文件
df_combined.to_csv('ADNI2_MRI&PET_ACPC_Y1&Y2.csv', index=False)