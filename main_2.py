from math import *
import pandas as pd
import numpy as np

x0 = -107.25
y0 = 11.664
a = 8
b = 8
miu = 1
lamda = 1.4
d_min = max(sqrt((a ** 2 + b ** 2)), b + 5)
h = miu * (a / 2)
d_r = lamda * d_min
m0 = ceil(100 / d_r)
m1 = ceil((350 + sqrt(x0 ** 2 + y0 ** 2) - 100) / d_r)
m2 = ceil((350 - sqrt(x0 ** 2 + y0 ** 2) - 100) / d_r)
left = [i for i in range(-m0 - m2, -m0)]
right = [i for i in range(m0, m0 + m1)]
rule = list(set(left).union(set(right)))
data = {"x": [], "y": [], "d_theta": [], "l_1": []}
data1 = {"x": [], "y": [], "i*d_theta": []}
for l in right:
    xi = x0 - (d_r*l)/sqrt(x0**2+y0**2)*x0
    yi = y0 - (d_r*l)/sqrt(x0**2+y0**2)*y0
    data["x"].append(xi)
    data["y"].append(yi)
    x_temp = ceil(2*pi*sqrt(xi**2+yi**2)/d_r)
    d_theta = 2*pi/x_temp
    if d_theta > 0.45 :
        d_theta = 0.4
    l_1 = ceil(2*pi/d_theta)
    data["l_1"].append(l_1)
    data["d_theta"].append(d_theta)

n = 0
for round in data["l_1"]:
    for i in range(0, round):
        center1 = np.array([[cos(i*data["d_theta"][n]), sin(i*data["d_theta"][n])], [-sin(i*data["d_theta"][n]), cos(i*data["d_theta"][n])]])
        center2 = np.array([data["x"][n]-x0, data["y"][n]-y0])
        center3 = np.dot(center1, center2)
        r = np.array([x0, y0]) + center3
        if sqrt(r[0]**2+r[1]**2) < 350 :
            data1["x"].append(r[0])
            data1["y"].append(r[1])
            data1["i*d_theta"].append(data["d_theta"][n])
    n += 1

# print(data)
df = pd.DataFrame(data1)
df.to_excel("point.xlsx")
