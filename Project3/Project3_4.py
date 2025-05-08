import numpy as np
import pandas as pd
import sys

delta_workday = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project3/weekday_delta.csv', index_col=0)) # 需求-实际
workday = np.abs(delta_workday).values.flatten().tolist()
name = ['北门', '体育馆', '计算机学院', '工程中心', '网球场', '菊苑1栋', '东门', '一食堂', '教学2楼', '二食堂', '教学4楼', '校医院', '梅苑1栋', '三食堂', '南门']
for na in range(len(name)):
    delta_workday.insert(0, name[len(name) - 1 - na], delta_workday.pop(name[len(name) - 1 - na]))
out = np.zeros((delta_workday.shape[1])) # 外运能力
im = np.zeros((delta_workday.shape[1])) # 运入需求
peaks = []
for i in range(6):
    peaks.append('2025-04-21 ' + ['08', '10', '12', '14', '18', '21'][i] + ':00:00')
print('For weekdays:')
cost_weekday = 0
num_weekday = 0
for time in peaks:
    print(f'- Regulation method for peak at {time}')
    for j in range(delta_workday.shape[1]):
        out[j] = int(-delta_workday.loc[time, delta_workday.columns[j]]) if delta_workday.loc[time, delta_workday.columns[j]] < 0 else 0
        im[j] = int(delta_workday.loc[time, delta_workday.columns[j]]) if delta_workday.loc[time, delta_workday.columns[j]] > 0 else 0

    dist = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project3/工作簿 2(Sheet1).csv', index_col=0))
    for i in range(dist.shape[0]):
        for j in range(i + 1):
            if j == i:
                dist.iloc[i, j] = 1e9+7
            else:
                dist.iloc[i, j] = dist.iloc[j, i]
    dist.columns = name
    dist.index = name
    time = np.round(dist / (25 / 3.6))

    R = np.zeros((delta_workday.shape[1], delta_workday.shape[1])) # 从i到j的收益
    for i in range(delta_workday.shape[1]):
        for j in range(delta_workday.shape[1]):
            R[i, j] = np.round(np.min((out[i], im[j], 20)) / time.iloc[i, j] * 1000)
    while np.max(R) != 0:
    # for _ in range(1):
        for i in range(delta_workday.shape[1]):
            for j in range(delta_workday.shape[1]):
                R[i, j] = np.round(np.min((out[i], im[j], 20)) / time.iloc[i, j] * 1000)
        i, j = np.argmax(R) // 15, np.argmax(R) % 15
        if i == j:
            break
        num = min((out[i], im[j]))
        pos = np.argmin((out[i], im[j]))
        if pos <= 1:
            out[i] -= num
            im[j] -= num
            print(f'-- Should move {int(num)} bikes from {name[i]} to {name[j]}. It takes {time.iloc[i, j]} seconds.')
        else:
            im[i] -= num
            out[j] -= num
            print(f'-- Should move {int(num)} bikes from {name[j]} to {name[i]}. It takes {time.iloc[i, j]} seconds.')
        cost_weekday += dist.iloc[i, j]
        num_weekday += 1
    print('================================================================')
#^ Workday

delta_weekend = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project3/weekday_delta.csv', index_col=0)) # 需求-实际
workday = np.abs(delta_weekend).values.flatten().tolist()
name = ['北门', '体育馆', '计算机学院', '工程中心', '网球场', '菊苑1栋', '东门', '一食堂', '教学2楼', '二食堂', '教学4楼', '校医院', '梅苑1栋', '三食堂', '南门']
for na in range(len(name)):
    delta_weekend.insert(0, name[len(name) - 1 - na], delta_weekend.pop(name[len(name) - 1 - na]))
out = np.zeros((delta_weekend.shape[1])) # 外运能力
im = np.zeros((delta_weekend.shape[1])) # 运入需求
peaks = []
for i in range(6):
    peaks.append('2025-04-21 ' + ['08', '10', '12', '14', '18', '21'][i] + ':00:00')
print('\n\nFor weekends:')
cost_weekend = 0
num_weekend = 0
for time in peaks:
    print(f'- Regulation method for peak at {time}')
    for j in range(delta_weekend.shape[1]):
        out[j] = int(-delta_weekend.loc[time, delta_weekend.columns[j]]) if delta_weekend.loc[time, delta_weekend.columns[j]] < 0 else 0
        im[j] = int(delta_weekend.loc[time, delta_weekend.columns[j]]) if delta_weekend.loc[time, delta_weekend.columns[j]] > 0 else 0

    dist = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project3/工作簿 2(Sheet1).csv', index_col=0))
    for i in range(dist.shape[0]):
        for j in range(i + 1):
            if j == i:
                dist.iloc[i, j] = 1e9+7
            else:
                dist.iloc[i, j] = dist.iloc[j, i]
    dist.columns = name
    dist.index = name
    time = np.round(dist / (25 / 3.6))

    R = np.zeros((delta_weekend.shape[1], delta_weekend.shape[1])) # 从i到j的收益
    for i in range(delta_weekend.shape[1]):
        for j in range(delta_weekend.shape[1]):
            R[i, j] = np.round(np.min((out[i], im[j], 20)) / time.iloc[i, j] * 1000)
    while np.max(R) != 0:
    # for _ in range(1):
        for i in range(delta_weekend.shape[1]):
            for j in range(delta_weekend.shape[1]):
                R[i, j] = np.round(np.min((out[i], im[j], 20)) / time.iloc[i, j] * 1000)
        i, j = np.argmax(R) // 15, np.argmax(R) % 15
        if i == j:
            break
        num = min((out[i], im[j]))
        pos = np.argmin((out[i], im[j]))
        if pos <= 1:
            out[i] -= num
            im[j] -= num
            print(f'-- Should move {int(num)} bikes from {name[i]} to {name[j]}. It takes {time.iloc[i, j]} seconds.')
        else:
            im[i] -= num
            out[j] -= num
            print(f'-- Should move {int(num)} bikes from {name[j]} to {name[i]}. It takes {time.iloc[i, j]} seconds.')
        cost_weekend += dist.iloc[i, j]
        num_weekend += 1
    print('================================================================')
#^ Weekend

#^ Problem 2

Q_weekday = np.array(pd.read_csv('.venv/Math_Modeling_MA206/Project3/周中共享单车分布插值表.csv', index_col=0))
D_weekday = np.array(pd.read_csv('.venv/Math_Modeling_MA206/Project3/weekday_delta.csv', index_col=0))
eta = 1 - (np.sum(np.abs(D_weekday)) / np.sum(Q_weekday))
cost = (cost_weekday + cost_weekend) / (num_weekday + num_weekend)
print(f'Eta is {eta}')
print(f'Cost is {cost}m per peak')
#^ Problem 3