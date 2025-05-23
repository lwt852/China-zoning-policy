# import pandas as pd


# def transform_and_save_to_excel(dataframe):
#     """
#     将输入的DataFrame数据进行转换，变成三列格式（两列索引对应值及它们对应位置的原始数据值），并保存为Excel文件。

#     参数:
#     dataframe (pd.DataFrame): 输入的原始DataFrame数据。

#     返回:
#     无
#     """
#     # 获取列名列表，去掉'Unnamed: 0'列（假设它是多余的索引列，可根据实际情况调整）
#     columns = [col for col in dataframe.columns if col!= 'Unnamed: 0']
#     new_data = []
#     # 双重循环遍历行列，构建新的数据结构
#     for i in range(len(columns)):
#         for j in range(len(columns)):
#             value = dataframe.iloc[i, j + 1]  # 获取对应位置的值，跳过'Unnamed: 0'这列
#             new_data.append([columns[i], columns[j], "", "", "", value])
  

#     # 将新数据转换为DataFrame
#     new_df = pd.DataFrame(new_data, columns=['Source','Target', 'Type', 'Id', 'Label','Weight'])    

#         # 排除第三列值小于0.5的行
#     new_df = new_df[new_df['Weight'] >= 0.43]

#     # print(new_df.dtypes)


#     new_df.to_excel(r'E:\桌面\黄河生态环境分区管控和高质量发展协同研究项目\数据\2020提取\指标del\第二次重做\MATLABzhibiao1-2space.xlsx', index=False)
#     # new_df.to_excel(r'E:\\桌面\\黄河生态环境分区管控和高质量发展协同研究项目\\数据\\2020提取\\corr_producespace', index=False)
#     # new_df.to_excel(r'E:\\桌面\\黄河生态环境分区管控和高质量发展协同研究项目\\数据\\2020提取\\all.xlsx', index=False)

# if __name__ == "__main__":
#     # 设置原始Excel文件路径（请根据实际情况替换为真实路径）
#     file_path = r'E:\桌面\黄河生态环境分区管控和高质量发展协同研究项目\数据\2020提取\指标del\第二次重做\MATLABzhibiao1.xlsx'
#     # file_path = r'E:\\桌面\\黄河生态环境分区管控和高质量发展协同研究项目\\数据\\2020提取\\corrmatrix - 副本.xls'
#     try:
#         # 读取原始Excel文件数据到DataFrame
#         sdg_rca = pd.read_excel(file_path)
#         # 调用函数进行数据转换并保存为新的Excel文件
#         transform_and_save_to_excel(sdg_rca)
#         print("数据转换并保存为Excel文件成功！")
#     except FileNotFoundError:
#         print(f"文件 {file_path} 不存在，请检查文件路径是否正确。")
#     except Exception as e:
#         print(f"出现其他错误: {e}")

import pandas as pd


def transform_and_save_to_excel(dataframe):
    """
    将输入的DataFrame数据进行转换，变成三列格式（两列索引对应值及它们对应位置的原始数据值），并保存为Excel文件。

    参数:
    dataframe (pd.DataFrame): 输入的原始DataFrame数据。

    返回:
    无
    """
    # 获取列名列表，去掉'Unnamed: 0'列（假设它是多余的索引列，可根据实际情况调整）
    columns = [col for col in dataframe.columns if col!= 'Unnamed: 0']
    new_data = []
    # 双重循环遍历行列，构建新的数据结构，添加更严谨的边界判断及异常捕获
    for i in range(len(columns)):
        for j in range(len(columns)):
            if j + 1 < len(dataframe.columns):
                try:
                    value = dataframe.iloc[i, j + 1]
                    new_data.append([columns[i], columns[j], "", "", "", value])
                except IndexError:
                    print(f"在处理索引i={i}, j={j}时出现索引越界问题，可检查此处逻辑")
    # 将新数据转换为DataFrame
    new_df = pd.DataFrame(new_data, columns=['Source', 'Target', 'Type', 'Id', 'Label', 'Weight'])
    print("筛选前new_df形状:", new_df.shape)
    # 排除第三列值小于0.5的行
    new_df = new_df[new_df['Weight'] >= 0.41]
    print("筛选后new_df形状:", new_df.shape)
    new_df.to_excel(r'E:\桌面\黄河生态环境分区管控和高质量发展协同研究项目\数据\2020提取\指标del\第四次重做\MATLABzhibiao1-2space.xlsx', index=False)
    # new_df.to_excel(r'E:\\桌面\\黄河生态环境分区管控和高质量发展协同研究项目\\数据\\2020提取\\corr_producespace', index=False)
    # new_df.to_excel(r'E:\\桌面\\黄河生态环境分区管控和高质量发展协同研究项目\\数据\\2020提取\\all.xlsx', index=False)


if __name__ == "__main__":
    # 设置原始Excel文件路径（请根据实际情况替换为真实路径）
    file_path = r'E:\桌面\黄河生态环境分区管控和高质量发展协同研究项目\数据\2020提取\指标del\第四次重做\MATLABzhibiao1.xlsx'
    # file_path = r'E:\\桌面\\黄河生态环境分区管控和高质量发展协同研究项目\\数据\\2020提取\\corrmatrix - 副本.xls'
    try:
        # 读取原始Excel文件数据到DataFrame
        sdg_rca = pd.read_excel(file_path)
        # 调用函数进行数据转换并保存为新的Excel文件
        transform_and_save_to_excel(sdg_rca)
        print("数据转换并保存为Excel文件成功！")
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在，请检查文件路径是否正确。")
    except Exception as e:
        print(f"出现其他错误: {e}")