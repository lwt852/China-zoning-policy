import numpy as np
import pandas as pd

def network_space(indicator_matrix, network_type):
    """
    计算指标之间相互作用的网络矩阵表示。

    输出：
        指标之间相互作用的网络矩阵表示。

    输入：
        (1) indicator_matrix：指标矩阵，其中每列代表一个指标，每行代表一个主体（如区域或个人）。
        (2) network_type：网络类型：
            (a) 'Product Space'：网络对应指标之间的互补性，如论文中所述：
                Hidalgo, César A., et al. "The product space conditions the development of nations." 
                Science 317.5837 (2007): 482-487.
            (b) 'Correlation'：网络对应指标之间的相关性，如论文中所述：
                Wu, Xutong, et al. "Decoupling of SDGs followed by re-coupling as sustainable development progresses." 
                Nature Sustainability 5.5 (2022): 452-459.

    注意：输入可以包含一些缺失变量！
    """

    # 将输入转换为NumPy数组（如果它是一个Pandas DataFrame）
    if isinstance(indicator_matrix, pd.DataFrame):
        indicator_matrix = indicator_matrix.values

    # 指标数量
    num_cols = indicator_matrix.shape[1]

    if network_type == 'Product Space':
        # 用列均值填充缺失值
        col_means = np.nanmean(indicator_matrix, axis=0)
        inds = np.where(np.isnan(indicator_matrix))
        indicator_matrix[inds] = np.take(col_means, inds[1])

        # 计算显性比较优势 (RCA)
        row_sums = np.sum(indicator_matrix, axis=1, keepdims=True)
        shares_1 = (1 / row_sums) * indicator_matrix
        shares_2 = np.sum(indicator_matrix, axis=0) / np.sum(indicator_matrix)
        rca = shares_1 / shares_2
        rca = rca > 1
        rca = rca.astype(int)  # 转换为整数

        # 构建网络矩阵
        rca_sums = np.sum(rca, axis=0)
        
        matrix1 = np.tile(rca_sums, (num_cols, 1))  # rca_sums延维度0重复num_cols次
        matrix2 = np.tile(rca_sums[:, np.newaxis], (1, num_cols))  # rca_sums延维度1重复num_cols次
        X = np.maximum(matrix1, matrix2)  # 两个矩阵逐元素最大值
        
        net_rca = (rca.T @ rca) / X
        np.fill_diagonal(net_rca, 0)
        
        return net_rca

    elif network_type == 'Correlation':
        # 构建网络矩阵
        net_corr = np.corrcoef(indicator_matrix, rowvar=False)
        np.fill_diagonal(net_corr, 0)  # 将对角线元素设置为0

        # 检查网络中是否存在缺失值
        if np.isnan(net_corr).any():
            print("相关性网络中存在缺失值。这可能是由于相关变量中缺失值过多导致的。请检查！")

        return net_corr

    else:
        print('不支持您的网络空间类型！')
        return None

# 示例用法
if __name__ == "__main__":
    # 创建示例数据
    np.random.seed(42)
    data = np.random.rand(100, 5)  # 100个样本，5个指标
    # 随机添加一些缺失值
    mask = np.random.random(data.shape) < 0.1
    data[mask] = np.nan
    
    # 使用DataFrame
    df = pd.DataFrame(data, columns=[f"指标{i+1}" for i in range(data.shape[1])])
    
    # 计算产品空间网络
    product_space = network_space(df, 'Product Space')
    print("产品空间网络矩阵:")
    print(product_space)
    
    # 移除相关网络的计算
    # corr_network = network_space(df, 'Correlation')
    # print("\n相关网络矩阵:")
    # print(corr_network)    