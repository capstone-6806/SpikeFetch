import pandas as pd
import matplotlib.pyplot as plt

# 从外部CSV文件读取数据
# 请将 'data.csv' 替换为你的实际文件名和路径
df = pd.read_csv('data.csv')

# 获取所有唯一的Trace名称
traces = df['Trace'].unique()

# 定义分类（SPEC 2017 和 Cloudsuite）
def get_category(trace):
    cloudsuite_traces = ['cloud9', 'cassandra', 'nutch', 'streaming']
    return 'Cloudsuite' if trace in cloudsuite_traces else 'SPEC 2017'

# 获取所有实验类型
exp_types = ['nopref', 'spp', 'bingo', 'mlop', 'dspatch', 'spp_ppf_dev', 'pythia', 'SpikeFetch']

# 为每种实验类型创建图表
for exp in exp_types[1:]:  # 从第二个开始（跳过 nopref，因为它是基准）
    fig, ax = plt.subplots(figsize=(18, 10))  # 增大图表大小
    
    # 获取nopref和当前exp的IPC值
    nopref_ipc = []
    exp_ipc = []
    categories = []
    for trace in traces:
        nopref_value = df[(df['Trace'] == trace) & (df['Exp'] == 'nopref')]['Core_0_IPC'].values[0]
        exp_value = df[(df['Trace'] == trace) & (df['Exp'] == exp)]['Core_0_IPC'].values[0]
        nopref_ipc.append(nopref_value)
        exp_ipc.append(exp_value)
        # 从 Cat 列获取分类
        category = df[(df['Trace'] == trace) & (df['Exp'] == 'nopref')]['Cat'].values[0]
        categories.append(category)
    
    # 设置柱状图宽度和位置
    bar_width = 0.42
    index = range(len(traces))
    
    # 创建柱状图
    bars1 = ax.bar(index, nopref_ipc, bar_width, label='nopref', color='#7f7f7f', alpha=1, zorder=4)
    bars2 = ax.bar([i + bar_width for i in index], exp_ipc, bar_width, label=exp, color='black', alpha=1, zorder=4)
    
    # 在柱状图上添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', 
                ha='center', va='bottom', fontsize=14)
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', 
                ha='center', va='bottom', fontsize=14)
    
    # 设置图表属性
    # ax.set_xlabel('Trace')
    ax.set_ylabel('IPC', fontsize=18)
    ax.set_title(f'IPC Comparison: nopref vs {exp}', fontsize=20)

    # 设置坐标轴文字大小
    ax.tick_params(axis='y', labelsize=16)
    ax.tick_params(axis='x', labelsize=16)
    
    # 设置 X 轴刻度标签为垂直显示
    ax.set_xticks([i + bar_width/2 for i in index])
    ax.set_xticklabels(traces, rotation=90, ha='center', fontsize=14)

    # 添加 Y 轴虚线网格
    ax.grid(axis='y', linestyle='--', alpha=0.8, zorder=1)
    
    # 添加分类边界和标签
    mcf_start = traces.tolist().index('605.mcf')  # Cloudsuite 开始位置
    cloudsuite_start = traces.tolist().index('cloud9')  # Cloudsuite 开始位置
    cloudsuite_end = traces.tolist().index('streaming')  # Cloudsuite 开始位置
    
    # 绘制分类分隔线（在 "cloud9" 左边，X 轴下方）
    ax.axvline(x=mcf_start - 0.8, color='black', linestyle='-', linewidth=0.8, clip_on=False, ymin=-0.3, ymax=0)
    ax.axvline(x=cloudsuite_start - 0.3, color='black', linestyle='-', linewidth=0.8, clip_on=False, ymin=-0.3, ymax=0)
    ax.axvline(x=cloudsuite_end + 1.22, color='black', linestyle='-', linewidth=0.8, clip_on=False, ymin=-0.3, ymax=0)
    
    # 添加分类标签（在 Trace 标签下方，字体加粗并加大）
    ax.text((cloudsuite_start + len(traces)) / 6, -0.38 * max(nopref_ipc, default=1), 'SPEC 2017', 
            ha='center', va='top', fontsize=14, fontweight='bold')
    ax.text((len(traces) + cloudsuite_start) / 2, -0.38 * max(nopref_ipc, default=1), 'Cloudsuite', 
            ha='center', va='top', fontsize=14, fontweight='bold')
  
    # 将图例移到最底部并横向展开
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2, frameon=False, fontsize=18)

    # ax.legend()
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(f'assets/ipc_comparison_{exp}.png')
    plt.close()

print("已生成6张对比图表，分别保存为 ipc_comparison_*.png")