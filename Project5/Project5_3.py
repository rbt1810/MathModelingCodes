from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)
app.json.ensure_ascii = False # 解决中文乱码问题

def recommend(score, rank, subject_type, major, school):
    subject_map = {
        'physics': '物理类',  # 根据实际数据调整
        'history': '历史类'   # 根据实际数据调整
    }
    subject_value = subject_map.get(subject_type, subject_type)
    df2 = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project5/data/2022.csv', index_col=0)).fillna('不可获取')
    df3 = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project5/data/2023.csv', index_col=0)).fillna('不可获取')
    df4 = pd.DataFrame(pd.read_csv('.venv/Math_Modeling_MA206/Project5/data/2024.csv', index_col=0)).fillna('不可获取')
    # rank = 10000
    df2 = df2[df2['科类'] == subject_value]
    df3 = df3[df3['科类'] == subject_value]
    df4 = df4[df4['科类'] == subject_value]
    df2 = df2[df2['院校专业与特殊信息'].str.contains(major)]
    df3 = df3[df3['院校专业与特殊信息'].str.contains(major)]
    df4 = df4[df4['院校专业与特殊信息'].str.contains(major)]
    df2 = df2[df2['院校专业与特殊信息'].str.contains(school)]
    df3 = df3[df3['院校专业与特殊信息'].str.contains(school)]
    df4 = df4[df4['院校专业与特殊信息'].str.contains(school)]
    range_size = max(500, int(rank * 0.2))
    rush2 = df2[(df2['最低位次'] <= rank) & (df2['最低位次'] >= max(1, rank - range_size))]
    stable2 = df2[(df2['最低位次'] >= rank) & (df2['最低位次'] <= rank + range_size)]
    save2 = df2[(df2['最低位次'] >= rank + range_size) & (df2['最低位次'] <= rank + 3 * range_size)]

    rush3 = df3[(df3['最低位次'] <= rank) & (df3['最低位次'] >= max(1, rank - range_size))]
    stable3 = df3[(df3['最低位次'] >= rank) & (df3['最低位次'] <= rank + range_size)]
    save3 = df3[(df3['最低位次'] >= rank + range_size) & (df3['最低位次'] <= rank + 3 * range_size)]

    rush4 = df4[(df4['最低位次'] <= rank) & (df4['最低位次'] >= max(1, rank - range_size))]
    stable4 = df4[(df4['最低位次'] >= rank) & (df4['最低位次'] <= rank + range_size)]
    save4 = df4[(df4['最低位次'] >= rank + range_size) & (df4['最低位次'] <= rank + 3 * range_size)]
    
    result = {
        "2022": {
            "冲": rush2.to_dict(orient='records'),
            "稳": stable2.to_dict(orient='records'),
            "保": save2.to_dict(orient='records')
        },
        "2023": {
            "冲": rush3.to_dict(orient='records'),
            "稳": stable3.to_dict(orient='records'),
            "保": save3.to_dict(orient='records')
        },
        "2024": {
            "冲": rush4.to_dict(orient='records'),
            "稳": stable4.to_dict(orient='records'),
            "保": save4.to_dict(orient='records')
        }
    }

    return result

@app.route('/')
def index():
    return render_template('mianchu.html')

# 修改端点名避免冲突
@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    try:
        data = request.json
        score = int(data['score'])
        rank = int(data['rank'])
        subject_type = data['subject_type']
        major = data['major']
        school = data['school']
        
        # 调用推荐函数
        res = recommend(score, rank, subject_type, major, school)
        # print(res)
        return jsonify({
            "success": True,
            "result": res
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"处理出错: {str(e)}"
        }), 400

if __name__ == '__main__':
    app.run(debug=True)