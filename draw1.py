import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# 生成二维高斯分布的数据
mean = [0, 0]
cov = [[1, 0], [0, 1]]
x = np.linspace(-1, 1, 8)
y = np.linspace(-1, 1, 8)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2) / 2) / (2 * np.pi * np.sqrt(1))

# 设置柱形图的参数
dx = dy = 0.2
dz = Z.flatten()
xpos, ypos = X.flatten(), Y.flatten()
num_elements = len(xpos)

# 计算渐变色
norm = plt.Normalize(dz.min(), dz.max())
colors = cm.viridis(norm(dz))

# 调整绘图区的大小
fig = plt.figure(figsize=(10, 8), dpi=100)  # 设置宽度为8英寸，高度为6英寸
ax = fig.add_subplot(111, projection='3d')

# 绘制柱形图
ax.bar3d(xpos, ypos, np.zeros(num_elements), dx, dy, dz, color=colors)

# 绘制方形环
min_x, max_x = np.min(xpos), np.max(xpos)
min_y, max_y = np.min(ypos), np.max(ypos)
min_z, max_z = np.min(dz), np.max(dz)

# 设置方形环的边长
side_length = 1.2

# 绘制高斯分布的全体方形环
ax.plot([mean[0]-side_length/2, mean[0]+side_length/2, mean[0]+side_length/2, mean[0]-side_length/2, mean[0]-side_length/2],
        [mean[1]-side_length/2, mean[1]-side_length/2, mean[1]+side_length/2, mean[1]+side_length/2, mean[1]-side_length/2],
        [0, 0, 0, 0, 0], 'r--', zorder=0)

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 设置初始视角
ax.view_init(elev=20, azim=40)

# 显示图形
plt.savefig("gauss.png")
plt.show()
