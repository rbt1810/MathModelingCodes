import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zhplot

#^ Problem 1
file = pd.DataFrame(pd.read_excel('.venv/Math_Modeling_MA206/Project4/附件(Attachment).xlsx', sheet_name='表1 (Table 1)'))
print(file)
plt.scatter(file.iloc[:, 1], file.iloc[:, 2])
plt.xlabel('时间（单位归一化）')
plt.ylabel('主路车流量')
plt.grid('both')
plt.show()

#^ Problem 2
file = pd.DataFrame(pd.read_excel('.venv/Math_Modeling_MA206/Project4/附件(Attachment).xlsx', sheet_name='表2 (Table 2)'))
print(file)
plt.scatter(file.iloc[:, 1], file.iloc[:, 2])
plt.xlabel('时间（单位归一化）')
plt.ylabel('主路车流量')
plt.grid('both')
plt.show()

#^ Problem 3
file = pd.DataFrame(pd.read_excel('.venv/Math_Modeling_MA206/Project4/附件(Attachment).xlsx', sheet_name='表3 (Table 3)'))
print(file)
plt.scatter(file.iloc[:, 1], file.iloc[:, 2])
plt.xlabel('时间（单位归一化）')
plt.ylabel('主路车流量')
plt.grid('both')
plt.show()

#^ Problem 4
file = pd.DataFrame(pd.read_excel('.venv/Math_Modeling_MA206/Project4/附件(Attachment).xlsx', sheet_name='表4 (Table 4)'))
print(file)
plt.scatter(file.iloc[:, 1], file.iloc[:, 2])
plt.xlabel('时间（单位归一化）')
plt.ylabel('主路车流量')
plt.grid('both')
plt.show()