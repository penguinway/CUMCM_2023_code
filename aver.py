import pandas as pd
from math import *

aver_yita_cos = []
sum_yita_cos = 0
list_yita_cos = []
months = [i for i in range(1, 13)]
times = [9, 10.5, 12, 13.5, 15]
result = {"yita_cos": []}
for i in range(1743, 1745):
    for month in months:
        for time in times:
            filename = str(month) + "_" + str(time) + ".xlsx"
            df = pd.read_excel(io=filename, sheet_name="Sheet1")
            sum_yita_cos += df.values[i][2]
    aver_yita_cos = sum_yita_cos / 60
    sum_yita_cos = 0
    list_yita_cos.append(aver_yita_cos)
result["yita_cos"] = list_yita_cos
df1 = pd.DataFrame(result)
df1.to_excel("result_power-and-yita.xlsx")
