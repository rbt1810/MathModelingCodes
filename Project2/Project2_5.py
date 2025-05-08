import pandas as pd
import numpy as np

df_loc = pd.read_excel('.venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls', sheet_name='附件1').iloc[2:, 0:5]
df_metal = pd.read_excel('.venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls', sheet_name='附件2').iloc[2:, :]
df_loc.columns = ['编号', 'x(m)', 'y(m)', '海拔(m)', '功能区']
df_metal.columns = ['编号', 'As (μg/g)', 'Cd (ng/g)', 'Cr (μg/g)', 'Cu (μg/g)', 'Hg (ng/g)', 'Ni (μg/g)', 'Pb (μg/g)', 'Zn (μg/g)']
df = pd.merge(df_loc, df_metal, on='编号')

bg = pd.read_excel('.venv/Math_Modeling_MA206/Project2/cumcm2011A附件_数据.xls', sheet_name='附件3').iloc[2:, 0:5]
bg.columns = ['metal', 'mean', 'sigma', 'range']

#^ Standardize the data
# for i in range(8):
#     mean = np.mean(df.iloc[:, i + 5])
#     sigma = np.std(df.iloc[:, i + 5])
#     df.iloc[:, i + 5] = (df.iloc[:, i + 5] - mean) / sigma
#     bg.iloc[i, 1] = (bg.iloc[i, 1] - mean) / sigma
# print(df)
# print(bg)

#^ 计算污染程度
I_geo = pd.DataFrame(np.zeros((319, 8)))
for i in range(I_geo.shape[0]):
    for j in range(I_geo.shape[1]):
        I_geo.iloc[i, j] = np.log2(df.iloc[i, j + 5] / (1.5 * bg.iloc[j, 1]))
# print(I_geo)
I_geo.columns = ['I_As', 'I_Cd', 'I_Cr', 'I_Cu', 'I_Hg', 'I_Ni', 'I_Pb', 'I_Zn']
polut = pd.concat([df.iloc[:, :5], I_geo], axis=1)
polut.to_csv('.venv/Math_Modeling_MA206/Project2/polut.csv', encoding='utf-8')
print(polut)

#^ 分析污染情况
analysis = pd.DataFrame(np.zeros((5, 8)))
analysis.index = ['生活区', '工业区', '山区', '交通区', '公园绿地区']
analysis.columns = ['I_As', 'I_Cd', 'I_Cr', 'I_Cu', 'I_Hg', 'I_Ni', 'I_Pb', 'I_Zn']
analysis['I_As'] = polut.groupby(by='功能区')['I_As'].mean().values
analysis['I_Cd'] = polut.groupby(by='功能区')['I_Cd'].mean().values
analysis['I_Cr'] = polut.groupby(by='功能区')['I_Cr'].mean().values
analysis['I_Cu'] = polut.groupby(by='功能区')['I_Cu'].mean().values
analysis['I_Hg'] = polut.groupby(by='功能区')['I_Hg'].mean().values
analysis['I_Ni'] = polut.groupby(by='功能区')['I_Ni'].mean().values
analysis['I_Pb'] = polut.groupby(by='功能区')['I_Pb'].mean().values
analysis['I_Zn'] = polut.groupby(by='功能区')['I_Zn'].mean().values
print(analysis)
analysis.to_csv('.venv/Math_Modeling_MA206/Project2/polut_analysis.csv',encoding='utf-8')

#^ 计算内梅罗指数
nml = pd.DataFrame(np.zeros((5, 1)))
nml_mean_As = polut.groupby(by='功能区')['I_As'].mean()
nml_mean_Cd = polut.groupby(by='功能区')['I_Cd'].mean()
nml_mean_Cr = polut.groupby(by='功能区')['I_Cr'].mean()
nml_mean_Cu = polut.groupby(by='功能区')['I_Cu'].mean()
nml_mean_Hg = polut.groupby(by='功能区')['I_Hg'].mean()
nml_mean_Ni = polut.groupby(by='功能区')['I_Ni'].mean()
nml_mean_Pb = polut.groupby(by='功能区')['I_Pb'].mean()
nml_mean_Zn = polut.groupby(by='功能区')['I_Zn'].mean()
# print(nml_mean_As.iloc[0])
nml_mean = pd.DataFrame(np.zeros((5, 1)))
# print(nml_mean.iloc[0])
for i in range(5):
    nml_mean.iloc[i] = np.mean([nml_mean_As.iloc[i], nml_mean_Cd.iloc[i], nml_mean_Cr.iloc[i], nml_mean_Cu.iloc[i], nml_mean_Hg.iloc[i], nml_mean_Ni.iloc[i], nml_mean_Pb.iloc[i], nml_mean_Zn.iloc[i]])
# print(nml_mean)

nml_max_As = polut.groupby(by='功能区')['I_As'].max()
nml_max_Cd = polut.groupby(by='功能区')['I_Cd'].max()
nml_max_Cr = polut.groupby(by='功能区')['I_Cr'].max()
nml_max_Cu = polut.groupby(by='功能区')['I_Cu'].max()
nml_max_Hg = polut.groupby(by='功能区')['I_Hg'].max()
nml_max_Ni = polut.groupby(by='功能区')['I_Ni'].max()
nml_max_Pb = polut.groupby(by='功能区')['I_Pb'].max()
nml_max_Zn = polut.groupby(by='功能区')['I_Zn'].max()
# print(nml_mean_As.iloc[0])
nml_max = pd.DataFrame(np.zeros((5, 1)))
# print(nml_mean.iloc[0])
for i in range(5):
    nml_max.iloc[i] = np.max([nml_max_As.iloc[i], nml_max_Cd.iloc[i], nml_max_Cr.iloc[i], nml_max_Cu.iloc[i], nml_max_Hg.iloc[i], nml_max_Ni.iloc[i], nml_max_Pb.iloc[i], nml_max_Zn.iloc[i]])
# print(nml_max)

for i in range(5):
    nml = np.sqrt(np.square(nml_max) + np.square(nml_mean) / 2)
nml.columns = ['内梅罗指数']
nml.index = ['生活区', '工业区', '山区', '交通区', '公园绿地区']
print(nml)


#? 计算富集因子
# EF = pd.DataFrame(np.zeros((319, 8)))
# for i in range(EF.shape[0]):
#     for j in range(EF.shape[1]):
#         EF.iloc[i, j] = () / ()