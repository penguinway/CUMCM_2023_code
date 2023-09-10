import math
import numpy as np
import pandas as pd
from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def cross(one, two):
    return one.x * two.x + one.y * two.y + one.z * two.z


def deplus(one, two):
    return Point(x=one.x - two.x, y=one.y - two.y, z=one.z - two.z)


def cal_turnc(a, b, r):
    theta = 4.5e-3
    h = 8
    R = 3.5
    r0 = (((sqrt(h ** 2 + (2 * R) ** 2) / 2) - (sqrt(a ** 2 + b ** 2)) / 2) / theta)
    if r <= r0:
        return 1
    if r > r0:
        x = (theta * r + sqrt(a ** 2 + b ** 2) / 2)
        return 2 * R * h / 2 * (x ** 2)


center_x = 0
center_y = 0
center_z = 0
a = 4.575
b = 4.575
H = 80
sum_yita = 0
sum1 = []
sum_power = 0
num = 3320
sum_eta_at = 0
sum_eta = 0
sum_eta_turn = 0


def inputs(points):
    df = pd.read_excel(io="001.xlsx", sheet_name="Sheet1", header=0)
    for i in range(0, num):
        point_ij = Point(x=-(df.values[i][0] / (sqrt(df.values[i][0] ** 2 + df.values[i][1] ** 2 + H ** 2))),
                         y=-(df.values[i][1] / (sqrt(df.values[i][0] ** 2 + df.values[i][1] ** 2 + H ** 2))),
                         z=H / (sqrt(df.values[i][0] ** 2 + df.values[i][1] ** 2 + H ** 2)))
        points.append(point_ij)
    return points


def calculate_DNI(altitude, sin_as):
    a = 0.4237 - 0.00821 * (np.power((6 - altitude), 2))
    b = 0.5055 + 0.00595 * (np.power((6.5 - altitude), 2))
    c = 0.2711 + 0.01858 * (np.power((2.5 - altitude), 2))
    DNI = 1.377 * (a + b * np.exp(-1 * (c / sin_as)))
    # 在这里实现根据纬度、海拔和太阳高度角，计算法向直接辐射辐照度DNI的代码
    return DNI


def calculate_thermal_power(DNI, eta, a, b):
    # 在这里实现计算定日镜场输出热功率的代码
    sum2 = a * b * eta
    thermal_powers = DNI * sum2
    return sum2


point = []
point = inputs(point)
months = [i for i in range(1, 13)]
D = [-59, -28, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275]
times = [9, 10.5, 12, 13.5, 15]
result = {"eta_at": [], "eta_ref": [], "eta_turnc": [], "eta_cos": [], "power": [], "eta": []}
for month in months:
    for time in times:
        sin_rou = sin((2 * pi * D[month - 1]) / 365) * sin((2 * pi * 23.45) / 360)
        omiga = (pi / 12) * (time - 12)
        sin_as = sqrt(1 - sin_rou ** 2) * cos((39.4 / 180) * pi) * cos(omiga) + sin_rou * sin((39.4 / 180) * pi)
        cos_ys = (sin_rou - sin_as * sin((39.4 / 180) * pi)) / sqrt(1 - sin_as ** 2) * cos((39.4 / 180) * pi)
        n_sun = Point(x=sqrt(1 - sin_as ** 2) * sqrt(1 - cos_ys ** 2), y=-1 * sqrt(1 - sin_as ** 2) * cos_ys,
                      z=-sin_as)
        for i in range(0, num):
            use_point = Point(point[i].x - center_x, point[i].y - center_y, point[i].z - center_z)
            # 点运算
            n = Point(0, 0, 0)
            n.x = (point[i].x - n_sun.x) / 2
            n.y = (point[i].y - n_sun.y) / 2
            n.z = (point[i].z - n_sun.z) / 2
            n1 = Point(x=n.x / sqrt(n.x ** 2 + n.y ** 2 + n.z ** 2),
                       y=n.y / sqrt(n.x ** 2 + n.y ** 2 + n.z ** 2),
                       z=n.z / sqrt(n.x ** 2 + n.y ** 2 + n.z ** 2))
            center = cross(n_sun, n1)
            yita_cos = cos(acos(-center) / 2)
            sum_yita += yita_cos
            dh = sqrt(use_point.x ** 2 + use_point.y ** 2 + use_point.z ** 2)
            eta_at = 0.99321 - 0.0001176 * dh + 1.97E-8 * dh ** 2
            sum_eta_at += eta_at
            eta = eta_at*cal_turnc(a, b, dh)*0.92*yita_cos
            sum_eta += eta
            sum_power += calculate_thermal_power(calculate_DNI(3, sin_as), eta, a, b)
            sum_eta_turn += cal_turnc(a, b, dh)
    dh = sqrt(use_point.x ** 2 + use_point.y ** 2 + use_point.z ** 2)
    eta_at = 0.99321 - 0.0001176 * dh + 1.97E-8 * dh ** 2
    result["eta_at"].append(sum_eta_at / (5*num))
    result["eta_ref"].append(0.92)
    result["eta_turnc"].append(sum_eta_turn / (5*num))
    result["eta_cos"].append(sum_yita / (5*num))
    result["eta"].append(sum_eta / (5*num))
    result["power"].append(sum_power / (5*num*a*b))
    sum_yita = 0
    sum_eta_at = 0
    sum_eta = 0
    sum_eta_turn = 0
print(sum_power / 60)
print(sum_power / (60*a*b*num))
df1 = pd.DataFrame(result)
file_name = "result_3_.xlsx"
df1.to_excel(file_name)
