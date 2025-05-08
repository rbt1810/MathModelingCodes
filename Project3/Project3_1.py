import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.interpolate import interp1d, PchipInterpolator

#^ Data Processing
columns = ['东门', '南门', '北门', '一食堂', '二食堂', '三食堂', '梅苑1栋', '菊苑1栋', '教学2楼', '教学4楼', '计算机学院', '工程中心', '网球场', '体育馆', '校医院']
index1 = pd.to_datetime(['7:30', '8:50', '11:10', '12:20', '13:50', '18:00', '21:20', '23:00'])
index2 = pd.to_datetime(['9:00', '12:00', '15:00', '18:00', '21:00'])
df1 = pd.DataFrame([[pd.NA, pd.NA, 24, pd.NA, 127, pd.NA, 97, 103, pd.NA, pd.NA, 3, pd.NA, 12, pd.NA, 11], 
                    [68, pd.NA, 66, 3, 8, pd.NA, 6, pd.NA, pd.NA, 157, pd.NA, 49, 22, 3, pd.NA], 
                    [pd.NA, pd.NA, pd.NA, 5, 19, 11, 15, 59, 200, pd.NA, 57, pd.NA, pd.NA, pd.NA, 25], 
                    [pd.NA, 66, 77, pd.NA, 122, pd.NA, 93, pd.NA, 18, pd.NA, 6, 2, pd.NA, 3, pd.NA], 
                    [43, pd.NA, 66, 10, pd.NA, pd.NA, 19, 62, pd.NA, 136, pd.NA, 70, 19, pd.NA, 35], 
                    [36, 99, pd.NA, pd.NA, 80, 65, pd.NA, pd.NA, 33, pd.NA, 59, pd.NA, pd.NA, 45, pd.NA], 
                    [103, pd.NA, 29, 27, pd.NA, pd.NA, 8, pd.NA, 104, 81, pd.NA, 72, pd.NA, 4, pd.NA], 
                    [pd.NA, 41, pd.NA, 85, 122, pd.NA, 113, pd.NA, pd.NA, 22, 17, pd.NA, 16, pd.NA, 13]])
df2 = pd.DataFrame([[31, 47, 15, pd.NA, 91, pd.NA, pd.NA, 106, pd.NA, 26, 4, pd.NA, pd.NA, pd.NA, pd.NA], 
                    [pd.NA, pd.NA, 57, 7, pd.NA, 7, 11, pd.NA, 200, pd.NA, pd.NA, 46, 17, pd.NA, pd.NA], 
                    [47, 38, 68, pd.NA, 19, pd.NA, pd.NA, pd.NA, pd.NA, 120, pd.NA, 61, 15, 0, pd.NA], 
                    [28, pd.NA, pd.NA, 110, 200, pd.NA, pd.NA, 91, 13, pd.NA, 6, 1, pd.NA, pd.NA, 3], 
                    [pd.NA, 29, pd.NA, 5, pd.NA, pd.NA, 19, 86, pd.NA, 138, 83, pd.NA, 9, 2, pd.NA], 
                    [pd.NA, 125, 72, pd.NA, pd.NA, 58, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, 48, 31, 6], 
                    [93, pd.NA, 19, pd.NA, 72, pd.NA, 7, 65, 109, pd.NA, 47, 83, pd.NA, pd.NA, 8], 
                    [19, 52, pd.NA, 80, 96, pd.NA, 143, pd.NA, 30, 13, pd.NA, 57, 15, pd.NA, 11]])
df3 = pd.DataFrame([[pd.NA, 44, 16, pd.NA, 97, pd.NA, pd.NA, 97, 19, 34, 0, pd.NA, 5, pd.NA, pd.NA], 
                    [pd.NA, pd.NA, 65, pd.NA, 11, pd.NA, 11, pd.NA, 200, 119, 48, 63, pd.NA, 1, 27], 
                    [62, 23, pd.NA, 7, pd.NA, 16, 23, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, 18, pd.NA, pd.NA], 
                    [pd.NA, pd.NA, 63, pd.NA, 137, pd.NA, pd.NA, 72, 30, pd.NA, 10, 4, 1, pd.NA, pd.NA], 
                    [64, pd.NA, pd.NA, 4, pd.NA, 12, 22, 52, pd.NA, 139, 76, pd.NA, pd.NA, 7, pd.NA], 
                    [pd.NA, 105, 72, pd.NA, 68, pd.NA, 67, pd.NA, 38, pd.NA, 38, pd.NA, pd.NA, 26, pd.NA], 
                    [pd.NA, pd.NA, pd.NA, 25, pd.NA, 57, 9, pd.NA, 118, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA], 
                    [9, pd.NA, pd.NA, pd.NA, 125, 123, pd.NA, 126, pd.NA, 24, pd.NA, 42, pd.NA, pd.NA, 8]])
df4 = pd.DataFrame([[pd.NA, pd.NA, 31, 54, pd.NA, 47, 106, 93, pd.NA, 34, 8, pd.NA, 37, pd.NA, 6], 
                    [86, 52, pd.NA, pd.NA, 58, 66, pd.NA, 66, 50, pd.NA, pd.NA, 38, pd.NA, 14, pd.NA], 
                    [146, pd.NA, 60, 14, pd.NA, 12, 28, pd.NA, pd.NA, 83, 24, pd.NA, pd.NA, 37, 2], 
                    [pd.NA, pd.NA, 125, pd.NA, 55, 52, pd.NA, pd.NA, pd.NA, 6, pd.NA, 29, 37, 67, pd.NA], 
                    [85, pd.NA, 46, 55, pd.NA, pd.NA, 119, 118, 31, pd.NA, 7, 43, 2, pd.NA, 1]])
df5 = pd.DataFrame([[78, 72, pd.NA, pd.NA, 43, pd.NA, pd.NA, pd.NA, 32, pd.NA, pd.NA, pd.NA, pd.NA, 34, pd.NA], 
                    [pd.NA, pd.NA, 102, 57, pd.NA, pd.NA, 52, pd.NA, pd.NA, pd.NA, 12, pd.NA, pd.NA, pd.NA, pd.NA], 
                    [pd.NA, pd.NA, pd.NA, pd.NA, 10, pd.NA, pd.NA, pd.NA, 82, pd.NA, pd.NA, 68, 30, pd.NA, pd.NA], 
                    [pd.NA, 103, pd.NA, pd.NA, pd.NA, pd.NA, 25, pd.NA, 3, pd.NA, 11, pd.NA, pd.NA, pd.NA, 3], 
                    [94, pd.NA, 38, pd.NA, 53, 47, pd.NA, pd.NA, pd.NA, 31, pd.NA, 55, pd.NA, 9, 1]])
df1.columns = columns
df2.columns = columns
df3.columns = columns
df4.columns = columns
df5.columns = columns
df1.index = index1
df2.index = index1
df3.index = index1
df4.index = index2
df5.index = index2

df_work = pd.DataFrame(np.zeros((df1.shape)))
df_work.columns = columns
df_work.index = index1
for i in range(df_work.shape[0]):
    for j in range(df_work.shape[1]):
        avg = pd.NA
        if pd.notna(df1.iloc[i, j]):
            avg = df1.iloc[i, j]
            if pd.notna(df2.iloc[i, j]):
                avg = np.mean((avg, df2.iloc[i, j]))
                if pd.notna(df3.iloc[i, j]):
                    avg = np.mean((avg, avg, df3.iloc[i, j]))
                    df_work.iloc[i, j] = avg
                    continue
                else: 
                    df_work.iloc[i, j] = avg
                    continue
            elif pd.notna(df3.iloc[i, j]):
                avg = np.mean((avg, df3.iloc[i, j]))
                df_work.iloc[i, j] = avg
                continue
            else:
                df_work.iloc[i, j] = avg
                continue
        elif pd.notna(df2.iloc[i, j]):
            avg = df2.iloc[i, j]
            if pd.notna(df3.iloc[i, j]):
                avg = np.mean((avg, df3.iloc[i, j]))
                df_work.iloc[i, j] = avg
                continue
            else:
                df_work.iloc[i, j] = avg
                continue
        elif pd.notna(df3.iloc[i, j]):
            avg = df3.iloc[i, j]
            df_work.iloc[i, j] = avg
            continue
        else:
            df_work.iloc[i, j] = avg
            continue

df_wkd = pd.DataFrame(np.zeros((df4.shape)))
df_wkd.columns = columns
df_wkd.index = index2
for i in range(df_wkd.shape[0]):
    for j in range(df_wkd.shape[1]):
        avg = pd.NA
        if pd.notna(df4.iloc[i, j]):
            avg = df4.iloc[i, j]
            if pd.notna(df5.iloc[i, j]):
                avg = np.mean((avg, df5.iloc[i, j]))
                df_wkd.iloc[i, j] = avg
                continue
            else:
                df_wkd.iloc[i, j] = avg
                continue
        elif pd.notna(df5.iloc[i, j]):
            avg = df5.iloc[i, j]
            df_wkd.iloc[i, j] = avg
            continue
        else:
            df_wkd.iloc[i, j] = avg
            continue
            

#^ Problem 1
# for i in df_work.columns:
#     valid_mask = df_work[i].notna()
#     x = df_work.index[valid_mask].astype(np.int64)
#     y = df_work[i][valid_mask]
#     f = interp1d(x, y, kind="cubic", fill_value="extrapolate")
#     df_work[i] = f(df_work.index.astype(np.int64))

for df in [df_work, df_wkd]:
    for col in df.columns:
        valid_mask = df[col].notna()
        x = df.index[valid_mask].astype(np.int64)
        y = df[col][valid_mask]
        
        # 处理空数据列
        if len(x) == 0:
            df[col] = 0  # 无数据时填充0
            continue
            
        # 动态选择插值方法
        if len(x) >= 4:
            # 使用PCHIP保形插值（天然避免过冲）
            f = PchipInterpolator(x, y, extrapolate=True)
        elif len(x) >= 2:
            # 使用线性插值并约束外推
            f = interp1d(x, y, kind='linear', 
                         fill_value=(min(y), max(y)),  # 外推值限制在已知范围内
                         bounds_error=False)
        else:
            # 单点数据使用常数填充
            df[col] = y.iloc[0] if len(x)==1 else 0
            continue
        
        # 执行插值
        interp_values = f(df.index.astype(np.int64))
        
        # 后处理
        interp_values = np.clip(interp_values, 0, None)  # 消除负数
        interp_values = np.where(interp_values < 0.1, 0, interp_values)  # 过滤微小值
        
        df[col] = interp_values
        df[col] = np.round(interp_values, 1)  # 保留1位小数

print(df_work)
df_work.to_csv('.venv/Math_Modeling_MA206/Project3/周中共享单车分布插值表.csv', )
# plt.plot(df_work.index, df_work.iloc[:, 0])
# plt.xlabel('Time')
# plt.ylabel('Number')
# plt.title(df_work.columns[0])
# plt.show()

# for i in df_wkd.columns:
#     valid_mask = df_wkd[i].notna()
#     x = df_wkd.index[valid_mask].astype(np.int64)
#     y = df_wkd[i][valid_mask]
#     if len(x) >= 4:
#         kind = 'cubic'
#     elif len(x) >= 2:
#         kind = 'linear'
#     else:
#         df_wkd[i] = df_wkd[i].ffill().bfill()
#         continue
#     f = interp1d(x, y, kind=kind, fill_value="extrapolate")
#     df_wkd[i] = f(df_wkd.index.astype(np.int64))

print(df_wkd)
df_wkd.to_csv('.venv/Math_Modeling_MA206/Project3/周末共享单车分布插值表.csv')
# df_interpolated.to_csv('.venv/Math_Modeling_MA206/Project3/共享单车分布插值表.csv')
# plt.plot(df_wkd.index, df_wkd.iloc[:, 0])
# plt.xlabel('Time')
# plt.ylabel('Number')
# plt.title(df_wkd.columns[0])
# plt.show()