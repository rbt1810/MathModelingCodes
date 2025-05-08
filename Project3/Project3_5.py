import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'SimHei'

name = ['北门', '体育馆', '计算机学院', '工程中心', '网球场', '菊苑1栋', '东门', '一食堂', '教学2楼', '二食堂', '教学4楼', '三食堂', '南门', '彩虹球场']
name2 = ['北门', '体育馆', '计算机学院', '工程中心', '网球场', '菊苑1栋', '东门', '一食堂', '教学2楼', '二食堂', '教学4楼', '三食堂', '南门', '彩虹球场', '仓库']
cangku = pd.DataFrame([634, 1151, 1040, 536, 1232, 1538, 1151, 1685, 1550, 2148, 1631, 1956, 2352, 2531, 0])
cangku.index = name2
dist = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project3/工作簿 2.csv', index_col=0)).iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15]]
for i in range(dist.shape[0]):
    dist.iloc[i, i] = 1e9+7
for i in range(dist.shape[0]):
    for j in range(i):
        dist.iloc[i, j] = dist.iloc[j, i]
dist.columns = name
dist.index = name

weekday = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project3/weekday_interpolated.csv', index_col=0))
weekday.loc[:, '彩虹球场'] = weekday.loc[:, '校医院'] + weekday.loc[:, '梅苑1栋']
weekday.drop(['校医院', '梅苑1栋'], axis=1, inplace=True)
bad = pd.DataFrame(np.round(weekday * 0.06))
# print(bad)
values = pd.DataFrame(np.zeros((dist.shape)))
times = pd.DataFrame(np.zeros((dist.shape)))
for t in range(bad.shape[1]):
    print(f'- On time {bad.index[t]}')
    for i in range(dist.shape[0]):
        for j in range(dist.shape[1]):
            values.iloc[i, j] = np.round(bad.iloc[t, j] / dist.iloc[i, j] * 10000)
            times.iloc[i, j] = np.around(dist.iloc[i, j] / 1000 / 25 * 60, 3)
    cangku_values = np.array(np.zeros(14))
    for i in range(len(cangku_values)):
        cangku_values[i] = np.round(bad.iloc[t, i] / cangku.iloc[i, 0] * 10000)
    # print(cangku_values)

    G = nx.Graph()
    for i in range(dist.shape[0]):
        for j in range(dist.shape[1]):
            if i == j:
                continue
            # G.add_weighted_edges_from([(name[i], name[j], {'values': values.iloc[i, j], 'bad': bad.iloc[i, j], 'time': times.iloc[i, j]})])
            G.add_weighted_edges_from([(name[i], name[j], values.iloc[i, j])], weight='values')
            G.add_weighted_edges_from([(name[i], name[j], bad.iloc[i, j])], weight='bad')
            G.add_weighted_edges_from([(name[i], name[j], times.iloc[i, j])], weight='time')
    for i in range(len(name)):
        G.add_weighted_edges_from([('仓库', name[i], np.round(bad.iloc[0, i] / cangku.iloc[i, 0] * 10000))], weight='values')
        G.add_weighted_edges_from([('仓库', name[i], bad.iloc[0, i])], weight='bad')
        G.add_weighted_edges_from([('仓库', name[i], np.around(cangku.iloc[i, 0] / 1000 / 25 * 60, 3))], weight='time')

    visit = pd.DataFrame(np.ones(15)) # 1为未访问
    visit.index = name2
    cur = '仓库'
    visit.loc[cur, 0] = 0 # 0为访问过
    total_time = 0
    total_bikes = 0
    while visit.astype(bool).any().any():
        visit.loc[cur, 0] = 0
        edges = G.edges(cur, data=True)
        max_value = 0
        to = None
        bikes = None
        time = None
        for _, v, data in edges:
            if data['values'] > max_value and visit.loc[v, 0] == 1:
                to = v
                max_value = data['values']
                bikes = data['bad']
                time = data['time']
        tmp = None
        if bikes != None:
            if total_bikes + bikes > 20:
                print(f' - Full! Should return to 仓库 to put bikes and go back to {to}. This takes {cangku.loc[to, 0] / 1000 / 25 * 60 * 2} minutes, and {to} remains {total_bikes - 20 + bikes} bikes.')
                total_time += cangku.loc[to, 0] / 1000 / 25 * 60 * 2
                total_bikes = total_bikes - 20 + bikes
                tmp = total_bikes
            else:
                total_bikes += bikes
        if to != None:
            if tmp != None:
                print(f' - Should go to {to}. This will add {tmp} bikes to the car. And it takes {time + bikes} minutes.')
            else:  
                print(f' - Should go to {to}. This will add {bikes} bikes to the car. And it takes {time + bikes} minutes.')
        if time != None:
            total_time += time + bikes
        cur = to
    print(f' - This path takes {total_time} minutes to go.')

# print(edges)

# pos = nx.circular_layout(G)
# # nx.draw(G, pos, with_labels=True, edge_color='b', node_color='g', node_size=1000)
# # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='c')
# T = nx.maximum_spanning_tree(G, weight='values')
# # print(T.edges())
# edge_labels = {
#     (u, v): f"bad: {T[u][v]['bad']}\ntime: {T[u][v]['time']}"  # 用换行符分隔两个属性
#     for u, v in T.edges()
# }
# total_time = np.sum(T[u][v]['time'] for u, v in T.edges())
# nx.draw(T, with_labels=True, pos=nx.circular_layout(G), edge_color='b', node_color='g', node_size=1000, width=2)
# pos = nx.circular_layout(T)
# nx.draw_networkx_edge_labels(T, pos, edge_labels=edge_labels, font_color='c')
# print(f'Total time is {np.around(total_time, 3)}')
# plt.show()