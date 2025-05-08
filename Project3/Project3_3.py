import pandas as pd
import numpy as np
import scipy
import queue

alpha = 0.7
beta = 0.3
result_weekday = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project3/weekday_interpolated.csv', index_col=0))
result_weekend = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project3/weekend_interpolated.csv', index_col=0))
print(result_weekday)
print(result_weekend)
S_day = []
demand_weekday = pd.DataFrame(np.zeros((result_weekday.shape)))
for i in range(result_weekday.shape[0]):
    S_day.append(np.sum(result_weekday.iloc[i]))
for i in range(result_weekday.shape[0]):
    for j in range(result_weekday.shape[1]):
        demand_weekday.iloc[i, j] = alpha * result_weekday.iloc[i, j] + beta * S_day[j] / result_weekday.shape[1]
demand_weekday.columns = result_weekday.columns
demand_weekday.index = result_weekday.index
delta_weekday = np.round(demand_weekday - result_weekday)
print(delta_weekday)
delta_weekday.to_csv('.venv/Math_Modeling_MA206/Project3/weekday_delta.csv')

S_day = []
demand_weekend = pd.DataFrame(np.zeros((result_weekend.shape)))
for i in range(result_weekend.shape[0]):
    S_day.append(np.sum(result_weekend.iloc[i]))
for i in range(result_weekend.shape[0]):
    for j in range(result_weekend.shape[1]):
        demand_weekend.iloc[i, j] = alpha * result_weekend.iloc[i, j] + beta * S_day[j] / result_weekend.shape[1]
demand_weekend.columns = result_weekend.columns
demand_weekend.index = result_weekend.index
delta_weekend = np.round(demand_weekend - result_weekend) # 需求-实际
print(delta_weekend)
delta_weekend.to_csv('.venv/Math_Modeling_MA206/Project3/weekend_delta.csv')