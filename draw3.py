from math import *
import pandas as pd
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mode(self):
        return sqrt(self.x ** 2 + self.y ** 2)


result = {"x": [], "y": []}
num = 3331
df = pd.read_excel("point12.xlsx", sheet_name="Sheet1")
points = []
points_new = []
for i in range(0, num):
    points.append(Point(df.values[i][1], df.values[i][2]))
for point in points:
    new = Point(
        x=(point.x * sqrt((point.x - 100/sqrt(point.x**2+point.y**2)*point.x)**2+(point.y - 100/sqrt(point.x**2 + point.y**2)*point.y)**2)/sqrt(point.x**2 + point.y**2)),
        y=(point.y * sqrt((point.x - 100/sqrt(point.x**2+point.y**2)*point.x)**2+(point.y - 100/sqrt(point.x**2 + point.y**2)*point.y)**2)/sqrt(point.x**2 + point.y**2)))
    points_new.append(new)
ooow = []
for i in range(0, len(points_new)):
    if sqrt(points_new[i].x**2+points_new[i].y**2) <= 350:
        ooow.append(points_new[i])
for oo in ooow:
    result["x"].append(oo.x)
    result["y"].append(oo.y)
df1 = pd.DataFrame(result)
df1.to_excel("123.xlsx")
