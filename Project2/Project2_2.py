import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df_loc = pd.read_excel('.venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls', sheet_name='附件1').iloc[2:, 0:5]
df_metal = pd.read_excel('.venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls', sheet_name='附件2').iloc[2:, :]
df_loc.columns = ['编号', 'x(m)', 'y(m)', '海拔(m)', '功能区']
df_metal.columns = ['编号', 'As (μg/g)', 'Cd (ng/g)', 'Cr (μg/g)', 'Cu (μg/g)', 'Hg (ng/g)', 'Ni (μg/g)', 'Pb (μg/g)', 'Zn (μg/g)']
df = pd.merge(df_loc, df_metal, on='编号')
# for i in df['功能区']:
#     if i == 1:
#         i = '生活区'
#     elif i == 2:
#         i = '工业区'
#     elif i == 3:
#         i = '山区'
#     elif i == 4:
#         i = '交通区'
#     elif i == 5:
#         i = '公园绿地区'
# print(df)

model = RandomForestClassifier(n_estimators=100, random_state=42)
# print(df.loc[:, ['x(m)', 'y(m)']])
# print(df.loc[:, '功能区'])
model.fit(df.loc[:, ['x(m)', 'y(m)']], df.loc[:, '功能区'].astype('int'))

# 生成全区网格点（假设地块范围为0-100）
xx, yy = np.meshgrid(np.linspace(0, 29000, 29001), np.linspace(0, 19000, 19001))
grid_elevation = np.random.rand(100, 100) * 500  # 假设全区高程数据

# 将网格点转换为特征矩阵
grid_X = np.column_stack([xx.ravel(), yy.ravel()])

# 预测功能区类别
grid_pred = model.predict(grid_X)
predicted_classes = grid_pred.reshape(xx.shape)

plt.figure(figsize=(10, 8))
plt.imshow(predicted_classes, extent=(0, 100, 0, 100), origin='lower', cmap='viridis')
plt.scatter(df['x'], df['y'], c=df['class'], edgecolor='k', cmap='viridis', s=50)
plt.colorbar(label='功能区类别')
plt.xlabel('X坐标')
plt.ylabel('Y坐标')
plt.title('基于随机森林的功能区插值')
plt.show()