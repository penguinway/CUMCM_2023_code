# 导入所需的库和模块
from math import *
import numpy as np
import pandas as pd

G0 = 1.366  # kw/m2
sum1 = []


# 计算太阳高度角𝛼𝑠和太阳方位角𝛾𝑠
# def calculate_solar_angles(day, time, latitude):
#     sin_rou = sin((day * np.pi * 2) / 365) * sin(((2 * np.pi) / 365) * 23.45)
#     omiga = (np.pi * (time - 12)) / 12
#     sin_as = (1 - sin_rou ** 2) * cos(latitude) * cos(omiga) + sin_rou * sin(latitude)
#     cos_ys = (sin_rou - sin_as * sin(latitude)) / (1 - sin_as ** 2) * cos(latitude)
#     # 在这里实现根据纬度和经度计算太阳高度角和太阳方位角的代码
#     solar_altitude = asin(sin_as)
#     solar_azimuth = acos(cos_ys)
#     return solar_altitude, solar_azimuth, sin_as


# 计算法向直接辐射辐照度DNI
def calculate_DNI(altitude, sin_as):
    a = 0.4237 - 0.00821 * (np.power((6 - altitude), 2))
    b = 0.5055 + 0.00595 * (np.power((6.5 - altitude), 2))
    c = 0.2711 + 0.01858 * (np.power((2.5 - altitude), 2))
    DNI = G0 * (a + b * np.exp(-1 * (c / sin_as)))
    # 在这里实现根据纬度、海拔和太阳高度角，计算法向直接辐射辐照度DNI的代码
    return DNI


# 计算光学效率𝜂
def calculate_optical_efficiency(yita_sb, yita_cos, yita_at, yita_trunc):
    # 阴影遮挡效率 𝜂sb = 1 − 阴影遮挡损失
    # 余弦效率 𝜂cos = 1 − 余弦损失
    # 大气透射率 𝜂at = 0.99321 − 0.0001176𝑑HR + 1.97 × 10−8 × 𝑑HR2  (𝑑HR ≤ 1000)
    # 集热器截断效率 𝜂trunc
    # E_acc 集热器接收能量,E_re 镜面全反射能量,E_a  阴影遮挡损失能量
    # 镜面反射率 𝜂ref
    yita_ref = 0.92
    optical_efficiency = []
    for i in range(1, 1744):
        optical_efficiency.append(yita_sb[i] * yita_cos[i] * yita_at[i] * yita_trunc[i] * yita_ref)
    # 在这里实现计算光学效率𝜂的代码
    return optical_efficiency


# 计算定日镜场的输出热功率
def calculate_thermal_power(DNI, optical_efficiency):
    # 在这里实现计算定日镜场输出热功率的代码
    xigma = 0
    for op in optical_efficiency:
        xigma += 36 * op
    thermal_powers = DNI * xigma
    sum1.append(thermal_powers)
    return thermal_powers


# 计算年平均光学效率和年平均输出热功率
# def calculate_average_efficiency_and_power(monthly_efficiencies, monthly_powers):
#     # 在这里实现计算年平均光学效率和年平均输出热功率的代码
#     annual_efficiency = sum(monthly_efficiencies) / len(monthly_efficiencies)
#     annual_power = sum(monthly_powers) / len(monthly_powers)
#     return annual_efficiency, annual_power
#
#
# # 计算单位镜面积年平均输出热功率
# def calculate_unit_area_power(mirror_area, average_power):
#     # 在这里实现计算单位镜面积年平均输出热功率的代码
#     unit_area_power = average_power / mirror_area
#     return unit_area_power


def main():
    yita_at = []
    df = pd.read_excel("附件.xlsx", sheet_name="Sheet1", header=1)
    for i in range(0, 1745):
        yita_at.append(df.values[i][3])
    months = [i for i in range(1, 13)]
    times = [9, 10.5, 12, 13.5, 15]
    yita_sb = []
    yita_trunc = []
    yita_cos = []
    optical_efficiency = []
    for month in months:
        for time in times:
            result = {"光学效率": [], "热功率": 0}
            df = pd.read_excel(str(month) + "_" + str(time) + ".xlsx")
            for i in range(0, 1745):
                yita_cos.append(df.values[i][3])
                yita_sb.append(df.values[i][4])
                yita_trunc.append(df.values[i][5])
            DNI = calculate_DNI(3, df.values[1][6])
            optical_efficiency = calculate_optical_efficiency(yita_sb, yita_cos, yita_at, yita_trunc)
            thermal_powers = calculate_thermal_power(DNI, optical_efficiency)
            result["光学效率"] = optical_efficiency
            result["热功率"] = thermal_powers
            df1 = pd.DataFrame(result)
            df1.to_excel("result_" + str(month) + "_" + str(time) + ".xlsx")
            yita_sb = []
            yita_trunc = []
            yita_cos = []
            optical_efficiency = []
    print(sum(sum1) / 60)

# 读取定日镜位置数据
# 遍历每个定日镜位置
# 根据位置计算太阳高度角𝛼𝑠和太阳方位角𝛾𝑠
# 根据纬度、海拔和太阳高度角，计算法向直接辐射辐照度DNI

# 计算光学效率𝜂
# 计算定日镜场输出热功率
# 将结果保存到表 1 中

# 计算年平均光学效率和年平均输出热功率
# 计算单位镜面积年平均输出热功率
# 将结果保存到表 2 中

# 输出结果或保存到文件


if __name__ == '__main__':
    main()
