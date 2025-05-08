import numpy as np
import pysal.lib as lw
from esda.moran import Moran
import matplotlib.pyplot as plt
import geopandas as gpd

def morans_i_analysis(coords, values, plot=True):
    """
    计算莫兰指数并输出分析报告
    参数：
        coords : np.array (n,2) - 采样点坐标[x,y]
        values : np.array (n,)  - 重金属浓度值
        plot : bool - 是否生成空间自相关图
    返回：
        moran : Moran对象 - 包含全部统计量
    """
    # 1. 构建空间权重矩阵（基于K近邻，k=5）
    k = 5
    w = lw.weights.KNN.from_array(coords, k=k)
    w.transform = 'r'  # 行标准化

    # 2. 计算莫兰指数
    moran = Moran(values, w, permutations=9999)  # 9999次蒙特卡洛模拟

    # 3. 输出统计报告
    print(f"莫兰指数 I = {moran.I:.3f}")
    print(f"P值 = {moran.p_sim:.4f}")
    print(f"Z得分 = {moran.z_sim:.3f}")
    print("--------------------------------")
    print(f"空间分布模式判定：")
    if moran.p_sim < 0.05:
        if moran.I > 0:
            print(f"显著空间正相关（聚集分布）")
        else:
            print(f"显著空间负相关（离散分布）")
    else:
        print(f"空间随机分布（无自相关）")

    # 4. 空间自相关可视化
    if plot:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 莫兰散点图
        lw.plot_moran(moran, zstandard=True, ax=ax)
        ax.set_title(f"Moran's I 分析结果 (I={moran.I:.2f}, p={moran.p_sim:.3f})")
        plt.tight_layout()
        
        # 空间分布热力图
        gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(coords[:,0], coords[:,1]))
        gdf['value'] = values
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        gdf.plot(column='value', cmap='YlOrRd', scheme='quantiles', 
                legend=True, ax=ax2, markersize=50)
        ax2.set_title("重金属浓度空间分布")
        plt.show()

    return moran

# 示例用法（替换为您的实际数据）
if __name__ == "__main__":
    # 模拟数据：100个采样点，工业区人为制造高值聚集
    np.random.seed(42)
    n_points = 100
    coords = np.random.rand(n_points, 2) * 100
    
    # 在左上角(20<x<40, 60<y<80)制造高浓度区
    industrial_mask = ((coords[:,0] > 20) & (coords[:,0] < 40) & (coords[:,1] > 60) & (coords[:,1] < 80))
    values = np.where(industrial_mask, 
                     np.random.lognormal(2, 0.3, n_points),  # 工业区高值
                     np.random.lognormal(0.5, 0.2, n_points)) # 其他区域低值
    
    # 执行分析
    moran = morans_i_analysis(coords, values)