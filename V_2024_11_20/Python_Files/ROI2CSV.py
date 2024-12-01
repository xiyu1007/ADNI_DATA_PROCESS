import csv

# 输入文件路径
input_file = 'AAL3v1_1mm.nii.txt'
# 输出文件路径
output_file = 'AAL3v1_1mm.csv'

# 表头行
header = ['ROIid;ROIabbr;ROIname;ROIcolor']

# 读取文件并转换
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    # 写入表头，将表头合并为一个单元格并写入
    outfile.write(';'.join(header) + '\n')

    # 逐行读取原始文件内容
    for line in infile:
        # 将每一行的数据合并为一个单元格
        parts = line.strip().split()

        # 合并所有数据为一个单元格
        row_data = ';'.join(parts)

        # 写入到输出文件中，将整个行写入一个单元格
        outfile.write(f'{row_data}\n')
