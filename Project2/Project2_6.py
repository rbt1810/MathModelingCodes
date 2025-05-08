from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

df_loc = pd.read_excel('.venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls', sheet_name='附件1').iloc[2:, 0:5]
df_loc.columns = ['编号', 'x(m)', 'y(m)', '海拔(m)', '功能区']
neighbour = NearestNeighbors()