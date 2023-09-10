import pandas as pd
from math import *

a = 6
b = 6
h = 8
theta = 4.5e-3
R = 3.5
datas = []
df = pd.read_excel(io="附件.xlsx", sheet_name="Sheet1", header=0)
# print(df.head())
for i in range(1, 1746):
    datas.append(df.values[i][2])
    # print(df.values[i][2])
result = {"yita": []}
r0 = (((sqrt(h ** 2 + (2 * R) ** 2) / 2) - (sqrt(a ** 2 + b ** 2)) / 2) / theta)
print(r0)
for data in datas:
    # print(data)
    if data <= r0:
        result["yita"].append(1)
    else:
        x = (theta * data + sqrt(a ** 2 + b ** 2) / 2)
        result["yita"].append(((2 * R * h) / (2 * (x**2))))
