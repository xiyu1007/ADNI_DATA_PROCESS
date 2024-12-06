import os

from tqdm import tqdm
import SimpleITK as sitk


def correct_bias_field(input_image_path, output_image_path, shrink_factor=1, mask_image_path=None,
                       iterations=0, fitting_levels=4):
    """ N4 偏置场校正到指定图像。 """

    # 读取输入图像，设定图像类型为 float32
    input_image = sitk.ReadImage(input_image_path, sitk.sitkFloat32)

    # 根据提供的掩膜图像路径读取掩膜图像（如果有）
    if mask_image_path:
        mask_image = sitk.ReadImage(mask_image_path, sitk.sitkUInt8)
    else:
        # 如果没有掩膜图像，则使用 Otsu 方法生成掩膜
        mask_image = sitk.OtsuThreshold(input_image, 0, 1, 200)

    # 根据收缩因子收缩输入图像和掩膜图像
    image = input_image
    if shrink_factor > 1:
        image = sitk.Shrink(input_image, [shrink_factor] * input_image.GetDimension())
        mask_image = sitk.Shrink(mask_image, [shrink_factor] * input_image.GetDimension())

    # 创建 N4 偏置场校正器
    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    # 如果提供了拟合层级数量参数，则更新相应值
    if iterations:
        corrector.SetMaximumNumberOfIterations([int(iterations)] * fitting_levels)

    # 执行偏置场校正
    corrected_image = corrector.Execute(image, mask_image)

    # 获取校正后的偏置场图像
    log_bias_field = corrector.GetLogBiasFieldAsImage(input_image)

    # 根据偏置场校正图像恢复全分辨率图像
    corrected_image_full_resolution = input_image / sitk.Exp(log_bias_field)

    # 写入全分辨率校正图像到输出文件
    sitk.WriteImage(corrected_image_full_resolution, output_image_path)

    # 如果收缩因子大于 1，则写入缩小的校正图像
    if shrink_factor > 1:
        sitk.WriteImage(corrected_image, "Python-Example-N4BiasFieldCorrection-shrunk.nrrd")


def batch_N4(in_folder, out_folder, endswith):
    log_file = r'.\N4_Error_Log.txt'

    shrink_factor = 1  # 可选，设置收缩因子
    mask_image_path = None  # 可选，掩膜图像路径，设置为 None 以使用 Otsu 方法
    number_of_iterations = 0  # 可选，设置迭代次数
    number_of_fitting_levels = 4  # 可选，设置拟合层级数量
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    for file_name in tqdm(os.listdir(in_folder), desc="Processing files"):
        if file_name.lower().endswith(tuple(endswith)):  # 识别以.dcm结尾的文件
            in_file = os.path.join(in_folder, file_name)
            out_file = os.path.join(out_folder, file_name)

            print('\n',"=" * 100)
            print("In: ", in_file)
            print("Out: ", out_file)
            try:
                # 调用函数进行偏置场校正
                correct_bias_field(in_file, out_file, shrink_factor, mask_image_path,
                                   number_of_iterations, number_of_fitting_levels)
            except Exception as e:
                with open(log_file, 'a') as f:
                    f.write(f"Error processing file {in_file}\n: {str(e)}\n")
                print(f"Error occurred during bias field correction:\n {in_file}")


if __name__ == "__main__":
    in_folder = rf"test"
    out_folder = "out_test"
    endswith = tuple('.nii')
    batch_N4(in_folder, out_folder, endswith)

    # ADNI = 'ADNI1'
    # Pre_Path = rf'D:\Matlab\Project\GroupMeeting'
    # out_folder = \
    #     rf"{Pre_Path}\Datasets_Filter_From_Raw\{ADNI}\N4"
    # AC_PC_Root = \
    #     rf"{Pre_Path}\Datasets_Filter_From_Raw\{ADNI}\AC-PC"
    # endswith = tuple('.nii')
    # Modality = ['MRI', 'PET']
    # # 记录开始时间
    # start_time = time.time()
    # print("Trying to use SimpleITK for bias field correction, which may take longer.")
    #
    # for m in Modality:
    #     in_folder = os.path.join(AC_PC_Root, m)
    #     m_out_folder = os.path.join(out_folder, m)
    #     if not os.path.exists(m_out_folder):
    #         os.makedirs(m_out_folder)
    #     batch_N4(in_folder, m_out_folder, endswith)
    # end_time = time.time()
    # # 计算运行时长
    # duration = end_time - start_time
    # print("偏置场校正完成。")
    #
    # formatted_duration = str(datetime.timedelta(seconds=duration))
    # print(f"运行时长: {formatted_duration}")
