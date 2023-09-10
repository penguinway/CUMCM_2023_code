from math import *
import pandas as pd
import numpy as np


x0 = -107.250
y0 = 11.664
num = 3320
df = pd.read_excel("123.xlsx", sheet_name="Sheet1")
result = {"h": [], "a": [], "b": [], "x": [], "y": []}
X = []
Y = []
for i in range(0, num):
    X.append(df.values[i][1])
    Y.append(df.values[i][2])
    result["x"].append(df.values[i][1])
    result["y"].append(df.values[i][2])
for i in range(0, num):
    r = sqrt((X[i]-x0)**2+(Y[i]-y0)**2)
    result["h"].append(14 - 12*np.exp(-r**2/(2*(500**2))))
    result["a"].append(4.575*(np.exp(r**2/(2*(500**2)))+1)/2)
    result["b"].append(4*(np.exp(r**2/(2*(500**2)))+1)/2)
df1 = pd.DataFrame(result)
df1.to_excel("1.xlsx")
