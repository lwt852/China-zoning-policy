import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.font_manager import FontManager, FontProperties

# ----------------------
# 彻底禁用 Arial 字体并强制使用中文字体
# ----------------------
plt.rcParams.update(plt.rcParamsDefault)
fm = FontManager()
fm.ttflist = [f for f in fm.ttflist if 'arial' not in f.name.lower()]
font_path = "C:/Windows/Fonts/simhei.ttf"  # 黑体字体路径
prop = FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

base_save_path = r'E:\桌面\黄河生态环境分区管控和高质量发展协同研究项目\数据\2020提取\指标del\第四次重做\pic3'
histogram_save_path = os.path.join(base_save_path, "histogram_plot.png")
describe_num_path = os.path.join(base_save_path, "describe_num_plot.png")
cdf_path = os.path.join(base_save_path, "cdf_plot.png")

def read_and_visualize_data(excel_file_path):
    try:
        data = pd.read_excel(excel_file_path)
        
        # 1. 直方图部分
        sns.set_style("white")
        mean = data["Weight"].mean()
        g = sns.histplot(data=data, x="Weight", alpha=0.5, kde=True)
        plt.axvline(mean, color='red', linestyle='--', label="平均值")
        plt.text(mean, 0.5, f'{mean:.2f}', ha='center', va='bottom', color='red', fontsize=10, fontproperties=prop)
        
        # 修复：安全获取图例句柄和标签
        handles, labels = plt.gca().get_legend_handles_labels()
        # 筛选包含"平均值"的图例项
        filtered_handles = [h for h, l in zip(handles, labels) if "平均值" in l]
        filtered_labels = [l for l in labels if "平均值" in l]
        
        if filtered_handles:  # 确保有匹配的图例项
            plt.legend(filtered_handles, filtered_labels, prop=prop)
        
        g.set_xlabel("协同值", fontproperties=prop)
        g.set_ylabel("计数", fontproperties=prop)
        g.figure.savefig(histogram_save_path, dpi=300, bbox_inches='tight')
        
        # 2. 描述性统计可视化部分
        describe_num_df = data[['Weight']].describe(include=['float64'])
        describe_num_df.reset_index(inplace=True)
        describe_num_df = describe_num_df[describe_num_df['index'] != 'count']
        
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        sns.stripplot(data=describe_num_df, x='index', y='Weight', ax=ax)
        ax.set_title('Weight 统计量', fontproperties=prop)
        ax.set_xlabel("统计量", fontproperties=prop)
        ax.set_ylabel("协同值", fontproperties=prop)
        weight_data = describe_num_df['Weight'].values
        ax.plot(range(len(weight_data)), weight_data, color='blue', linestyle='-', marker='o')
        plt.tight_layout()
        fig.savefig(describe_num_path, dpi=300, bbox_inches='tight')
        
        # 3. 累积分布函数（CDF）图
        stats_df = data.groupby('Weight')['Weight'].agg('count').pipe(pd.DataFrame).rename(columns={'Weight': 'frequency'})
        stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
        stats_df['cdf'] = stats_df['pdf'].cumsum()
        stats_df = stats_df.reset_index()
        
        cg = stats_df.plot(x='Weight', y=['cdf'], grid=True)
        cg.set_xlabel("协同值", fontproperties=prop)
        cg.set_ylabel("累积概率", fontproperties=prop)
        cg.figure.set_facecolor("white")
        cg.grid(False)
        cg.figure.savefig(cdf_path, dpi=300, bbox_inches='tight')
        
        print("数据读取及可视化操作成功！")
    except FileNotFoundError:
        print(f"文件 {excel_file_path} 不存在，请检查文件路径是否正确。")
    except Exception as e:
        print(f"出现其他错误: {e}")
        import traceback
        traceback.print_exc()  # 打印详细错误堆栈

if __name__ == "__main__":
    excel_file_path = r'E:\桌面\黄河生态环境分区管控和高质量发展协同研究项目\数据\2020提取\指标del\第七次重做\MATLABzhibiao1-all.xlsx'
    read_and_visualize_data(excel_file_path)