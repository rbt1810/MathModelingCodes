import pandas as pd
import numpy as np
from scipy.interpolate import griddata, RBFInterpolator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import LabelEncoder
from matplotlib.cm import get_cmap

plt.rcParams['font.sans-serif'] = ['HarmonyOS Sans SC']  # 指定默认字体为黑体

# 读取数据
df_loc = pd.read_excel('.venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls', sheet_name='附件1').iloc[2:, 0:5]
df_metal = pd.read_excel('.venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls', sheet_name='附件2').iloc[2:, :]
df_loc.columns = ['编号', 'x(m)', 'y(m)', '海拔(m)', '功能区']
df_metal.columns = ['编号', 'As (μg/g)', 'Cd (ng/g)', 'Cr (μg/g)', 'Cu (μg/g)', 'Hg (ng/g)', 'Ni (μg/g)', 'Pb (μg/g)', 'Zn (μg/g)']
# print(df_loc)
# print(df_metal)

# 合并数据
df = pd.merge(df_loc, df_metal, on='编号')

# 创建插值网格
x = df['x(m)']
y = df['y(m)']
xi = np.linspace(x.min(), x.max(), 500)
yi = np.linspace(y.min(), y.max(), 500)
xi, yi = np.meshgrid(xi, yi)

# 海拔插值
# zi_alt = griddata((x, y), df['海拔(m)'], (xi, yi), method='cubic')

# 创建RBF插值器（调整平滑参数）
rbf = RBFInterpolator(
    np.vstack([x, y]).T, 
    df['海拔(m)'],
    kernel='thin_plate_spline',
    smoothing=1.0  # 增大平滑参数抑制震荡
)
zi_alt = rbf(np.vstack([xi.ravel(), yi.ravel()]).T).reshape(xi.shape)

#^ 绘制三维地形图
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(xi, yi, zi_alt, cmap='terrain', alpha=0.8)
# ax.set_xlabel('X (m)')
# ax.set_ylabel('Y (m)')
# ax.set_zlabel('Altitude (m)')
# plt.title('三维地形图')
# plt.show()

# 金属元素插值示例（以As为例）
metal = 'Pb (μg/g)'
# zi_metal = griddata((x, y), df[metal], (xi, yi), method='cubic')

# 创建RBF插值器（调整平滑参数）
rbf = RBFInterpolator(
    np.vstack([x, y]).T, 
    df[metal],
    kernel='thin_plate_spline',
    smoothing=1.0  # 增大平滑参数抑制震荡
)
zi_metal = rbf(np.vstack([xi.ravel(), yi.ravel()]).T).reshape(xi.shape)

encoder = LabelEncoder()
labels = encoder.fit_transform(df['功能区'])
region_names = ['商业区', '住宅区', '工业区', '绿化区', '交通枢纽']
cmap = get_cmap('viridis', 5)  # 使用预定义颜色映射

# 绘制热力图
plt.figure(figsize=(10, 8))
contour = plt.contourf(xi, yi, zi_metal, levels=20, cmap='RdYlGn_r')
scatter = plt.scatter(x, y, c=labels, cmap=cmap, s=15, alpha=1, edgecolors='k', label=df['功能区'])  # 显示采样点
plt.colorbar(contour).set_label(f'{metal}浓度')
# plt.legend(handles=, )
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title(f'{metal}浓度分布热力图')
plt.show()