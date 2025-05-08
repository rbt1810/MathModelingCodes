import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.interpolate import NearestNDInterpolator

# 读取数据（假设已加载为DataFrame）
df = pd.read_excel(".venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls", sheet_name="附件1")
df_concentration = pd.read_excel(".venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls", sheet_name="附件2")

# 合并数据
merged_df = pd.merge(df[['编号', 'x(m)', 'y(m)', '功能区']], 
                    df_concentration, 
                    on='编号')

# 提取坐标、功能区和浓度数据（以As为例）
points = merged_df[['x(m)', 'y(m)']].values
zones = merged_df['功能区'].values
as_concentration = merged_df['As (μg/g)'].values

# 生成覆盖整个区域的网格
x_min, x_max = points[:,0].min(), points[:,0].max()
y_min, y_max = points[:,1].min(), points[:,1].max()
grid_x, grid_y = np.meshgrid(
    np.linspace(x_min, x_max, 100), 
    np.linspace(y_min, y_max, 100)
)
grid_points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T

# 阶段1：预测网格点的功能区（最近邻分类）
zone_classifier = NearestNeighbors(n_neighbors=1)
zone_classifier.fit(points)
_, indices = zone_classifier.kneighbors(grid_points)
predicted_zones = zones[indices.flatten()]

# 阶段2：分功能区进行浓度插值
interpolated_values = np.full(grid_points.shape[0], np.nan)

for zone in np.unique(zones):
    # 获取当前功能区的采样点
    mask = (zones == zone)
    zone_points = points[mask]
    zone_values = as_concentration[mask]
    
    if len(zone_points) == 0:
        continue
    
    # 训练当前功能区的插值器
    interpolator = NearestNDInterpolator(zone_points, zone_values)
    
    # 对属于该功能区的网格点插值
    zone_mask = (predicted_zones == zone)
    if zone_mask.any():
        interpolated_values[zone_mask] = interpolator(
            grid_points[zone_mask]
        )

# 处理未覆盖区域（用全局最近邻填充）
global_interpolator = NearestNDInterpolator(points, as_concentration)
nan_mask = np.isnan(interpolated_values)
interpolated_values[nan_mask] = global_interpolator(
    grid_points[nan_mask]
)

# 重塑为网格形状
result_grid = interpolated_values.reshape(grid_x.shape)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
# 绘制插值结果
contour = plt.contourf(grid_x, grid_y, result_grid, cmap='viridis')
# 叠加采样点和功能区标签
scatter = plt.scatter(
    points[:,0], points[:,1], 
    c=zones, edgecolor='k', 
    cmap='tab20', label='采样点功能区'
)
plt.colorbar(contour, label='As浓度 (μg/g)')
plt.colorbar(scatter, label='功能区分类')
plt.title("基于功能区的最近邻插值结果")
plt.show()