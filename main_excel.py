import math

import pandas as pd
from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def cross(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z


def inputs(points):
    df = pd.read_excel(io="附件.xlsx", sheet_name="Sheet2", header=0)
    for i in range(1, 1746):
        point_ij = Point(x=-(df.values[i][0] / (sqrt(df.values[i][0] ** 2 + df.values[i][1] ** 2 + 80 ** 2))),
                         y=-(df.values[i][1] / (sqrt(df.values[i][0] ** 2 + df.values[i][1] ** 2 + 80 ** 2))),
                         z=80 / (sqrt(df.values[i][0] ** 2 + df.values[i][1] ** 2 + 80 ** 2)))
        points.append(point_ij)
    return points


def deplus(a, b):
    return Point(x=(a.x - b.x) / 2, y=(a.y - b.y) / 2, z=(a.z - b.z) / 2)



point = []
point = inputs(point)
months = [i for i in range(1, 13)]
D = [-59, -28, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275]
times = [9, 10.5, 12, 13.5, 15]
a = 0
result = {"yita_cos": []}
sum_yita = 0
for i in range(0, 1745):
    for month in months:
        for time in times:
            sin_rou = sin((2 * pi * D[month-1]) / 365) * sin((2 * pi * 23.45) / 360)
            omiga = (pi / 12) * (time - 12)
            sin_as = sqrt(1 - sin_rou ** 2) * cos((39.4 / 180) * pi) * cos(omiga) + sin_rou * sin((39.4 / 180) * pi)
            cos_ys = (sin_rou - sin_as * sin((39.4 / 180) * pi)) / sqrt(1 - sin_as ** 2) * cos((39.4 / 180) * pi)
            n_sun = Point(x=sqrt(1 - sin_as ** 2) * sqrt(1 - cos_ys ** 2), y=-1 * sqrt(1 - sin_as ** 2) * cos_ys, z=-sin_as)
            n = Point(0, 0, 0)
            n.x = (point[i].x - n_sun.x) / 2
            n.y = (point[i].y - n_sun.y) / 2
            n.z = (point[i].z - n_sun.z) / 2
            n1 = Point(x=n.x / sqrt(n.x ** 2 + n.y ** 2 + n.z ** 2),
                       y=n.y / sqrt(n.x ** 2 + n.y ** 2 + n.z ** 2),
                       z=n.z / sqrt(n.x ** 2 + n.y ** 2 + n.z ** 2))
            # result["n_sun"].append((n_sun.x, n_sun.y, n_sun.z))
            # result["m0"].append((n1.x, n1.y, n1.z))
            # result["sin_as"].append(sin_as)
            # result["cos_ys"].append(cos_ys)
            # result["yita_sb"].append(1)
            # result["yita_trunc"].append(1)
            center = cross(n_sun, n1)
            yita_cos = cos(acos(-center) / 2)
            sum_yita += yita_cos
    result["yita_cos"].append(sum_yita/60)
    sum_yita = 0
df1 = pd.DataFrame(result)
file_name = "result_trunc.xlsx"
df1.to_excel(file_name)
