import pandas as pd
from scipy.interpolate import interp1d

# 读取数据并预处理
df_weekend = pd.read_csv(".venv/Math_Modeling_MA206/Project3/周末共享单车分布插值表.csv", parse_dates=[0], index_col=0)
df_weekday = pd.read_csv(".venv/Math_Modeling_MA206/Project3/周中共享单车分布插值表.csv", parse_dates=[0], index_col=0)

def interpolate_extrapolate(df, start_hour=7, end_hour=23):
    # 生成目标时间范围（每小时一个点）
    full_index = pd.date_range(f"{df.index.date[0]} {start_hour}:00", 
                               f"{df.index.date[0]} {end_hour}:00", freq='H')
    
    # 创建一个空的DataFrame，索引为完整时间范围
    interpolated_df = pd.DataFrame(index=full_index, columns=df.columns)
    
    # 线性插值外推
    for col in df.columns:
        x = df.index.hour + df.index.minute/60  # 原始时间点（小时小数形式）
        y = df[col].values
        
        # 如果数据点不足2个，直接填充0或均值
        if len(x) < 2:
            interpolated_df[col] = y[0] if len(y) > 0 else 0
            continue
        
        # 创建插值函数（允许外推）
        f = interp1d(x, y, kind='linear', fill_value="extrapolate")
        
        # 生成预测时间点（小时小数形式）
        new_x = full_index.hour + full_index.minute/60
        
        # 应用插值并赋值
        interpolated_df[col] = f(new_x)
    
    # 非负处理
    interpolated_df = interpolated_df.clip(lower=0)
    return interpolated_df

# 生成结果
result_weekend = interpolate_extrapolate(df_weekend)
result_weekday = interpolate_extrapolate(df_weekday)
# 四舍五入周中和周末的结果
result_weekend = result_weekend.round().astype(int)
result_weekday = result_weekday.round().astype(int)
print(result_weekday)
print(result_weekend)
result_weekday.to_csv('.venv/Math_Modeling_MA206/Project3/weekday_interpolated.csv')
result_weekend.to_csv('.venv/Math_Modeling_MA206/Project3/weekend_interpolated.csv')
#^ Problem 1