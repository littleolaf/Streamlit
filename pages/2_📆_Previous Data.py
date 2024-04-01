import pandas as pd
from datetime import datetime, date
import streamlit as st
from streamlit_echarts import st_echarts
from pages.data.load_data import load_data

# 设置网页信息
st.set_page_config(page_title="FAU System Data Display", page_icon=":chart_increasing:📈",layout='wide')
# 设置网页标题，开始布局
# st.title("Previous Data Display")  # 更改为自定义样式markdown语法
st.markdown(f"<h1 style='text-align: center;'>Previous Data Display</h1>", unsafe_allow_html=True)
# 获取数据帧
data = load_data()
first_record_date = data["Humidity"][0]
# 设置日期选择器的标签、初始值和最小/最大日期范围
start_date, end_date = st.sidebar.date_input('Select the time period',
                                             value=(datetime(2023, 5, 18), date.today()),
                                             min_value=first_record_date,
                                             max_value=date.today(),
                                             help='Please select the period you want to search')
start_date = pd.to_datetime(start_date, dayfirst=True)  # datetime.date转为timestamp类型便于选择与查找
end_date = pd.to_datetime(end_date, dayfirst=True) + pd.DateOffset(days=1)  # datetime.date转为timestamp类型便于选择与查找
# 打印用户选择的日期
# st.write('You selected:', start_date)
# 获取日期段内的数据
data = data[(data["Humidity"] > start_date) & (data["Humidity"] < end_date)]
# Line chart
st.write('\n')
option = {
    # 鼠标悬浮图释,悬浮窗
    'tooltip': {
        'trigger': 'axis',
        'axisPointer': {
            'type': 'line',
            'animation': False,
            'label': {
                'backgroundColor': '#505765'
            }
        }
    },
    # 图例
    'legend': {
        # 'data': ['Email']
    },
    # 右上角工具栏
    'toolbox': {
        'show': True,
        'feature': {
            'dataZoom': {
                'yAxisIndex': 'none'
            },
            # 'dataView': {'readOnly': False},
            'magicType': {'type': ['line', 'bar']},
            'restore': {},
            'saveAsImage': {}
        }
    },
    # 数据选区范围工具
    'dataZoom': [
        {
            'show': True,
            'type': 'slider',
            'realtime': True,
            'start': 0,
            'end': 100
        },
        {
            'type': 'inside',
            'realtime': True,
            'start': 0,
            'end': 100
        }
    ],
    'xAxis': {
        'name': 'Time line',
        'type': 'category',
        'data': data["Temperature"].tolist()
    },
    # 双y轴
    'yAxis': [
        {
            'name': 'Humidity(%)',
            'type': 'value'
        },
        {
            'name': 'Temperature(°C)',
            'type': 'value'
        }
    ],
    'series': [
        {
            'name': 'Humidity',
            'data': data['Window'].tolist(),
            'type': 'line',
            'smooth': True
        },
        {
            'name': 'Temperature',
            'data': data['Window.1'].tolist(),
            'type': 'line',
            'smooth': True
        }
    ]
}
st_echarts(options=option)
# Raw data
st.write('\n')
with st.expander("Raw Data"):
    st.dataframe(data)
