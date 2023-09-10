import pandas as pd
import numpy as np
from scipy.optimize import differential_evolution

# 读取定日镜位置数据
position_data = pd.read_excel('position_data.xlsx')

# 设计参数范围
mirror_width_range = (2, 8)  # 镜面宽度范围
install_height_range = (2, 6)  # 安装高度范围


# 目标函数，计算单位镜面积年平均输出热功率与额定功率之间的差值
def objective_function(x):
    mirror_width = x[0]
    install_height = x[1]

    # 根据镜面宽度和安装高度计算镜面数量和总面积
    mirror_num = len(position_data)
    mirror_area = mirror_num * mirror_width * mirror_height

    # 计算单位镜面积年平均输出热功率
    output_power = calculate_output_power(mirror_area, efficiency)

    abs_diff = np.abs(output_power - 60)  # 根据问题3，额定功率为60MW
    return abs_diff


# 参数范围
bounds = [mirror_width_range, install_height_range]

# 调用优化算法求解
result = differential_evolution(objective_function, bounds)
optimal_params = result.x  # 最优参数

# 将结果保存到result3.xlsx文件中
df_result = pd.DataFrame({'Mirror Width': [optimal_params[0]],
                          'Install Height': [optimal_params[1]],
                          'Abs_Difference': [result.fun]})

with pd.ExcelWriter('result3.xlsx') as writer:
    df_result.to_excel(writer, sheet_name='Sheet1', index=False)
