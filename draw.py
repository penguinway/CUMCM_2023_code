import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from matplotlib import cm
import numpy as np

# 创建一个三维坐标系
fig = plt.figure(figsize=(8, 6), dpi=200)
ax = plt.axes(projection='3d')

df = pd.read_excel("point12.xlsx", sheet_name="Sheet1")
# 生成数据
x = []
y = []
z = []
for i in range(0, 3330):
    x.append(df.values[i][1])
    y.append(df.values[i][2])
    z.append(df.values[i][3])
X = np.array(x)
Y = np.array(y)
Z = np.array(z)

# 绘制三维散点图
scatter = ax.scatter(x, y, z, c=z, cmap="jet")
# ax.plot_surface(X, Y, Z, cmap='rainbow')

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=90, azim=270)
fig.colorbar(scatter)
# 显示图形
plt.savefig("eta_cos30_2.png")
plt.show()
