import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts
from pages.data.load_data import load_data, realTime, get_position

# 1_🏠_Home
def Energy(location,position):
    today = 199
    yesterday = 208
    return today, yesterday
def Temperature_chart(value):
    # todo: 根据温度具体值修改显示颜色
    option = {
        'tooltip': {
            'formatter': '{b} : {c} °C'
        },
        'series': [
            {
                'type': 'gauge',
                # 设置图表的中心位置，相对于图表容器的百分比位置
                'center': ['50%', '60%'],
                'startAngle': 220,
                'endAngle': -40,
                'min': 0,
                'max': 40,
                'splitNumber': 10,
                'itemStyle': {
                    'color': '#FFAB91'
                },
                # 进度条的样式和行为
                'progress': {
                    'show': True,
                    'width': 20
                },
                'pointer': {
                    'show': True
                },
                'axisLine': {
                    'lineStyle': {
                        'width': 20
                    }
                },
                # 刻度线的样式和行为
                'axisTick': {
                    'distance': -40,
                    'splitNumber': 4,
                    'lineStyle': {
                        'width': 2,
                        'color': '#999'
                    }
                },
                'splitLine': {
                    'distance': -47,
                    'length': 14,
                    'lineStyle': {
                        'width': 3,
                        'color': '#999'
                    }
                },
                'axisLabel': {
                    'distance': -20,
                    'color': '#999',
                    'fontSize': 20
                },
                'anchor': {'show': False},
                'title': {'show': True  # ,'color': '#FFAB91'
                          },
                'detail': {
                    'valueAnimation': True,
                    'width': '60%',
                    'lineHeight': 40,
                    'borderRadius': 8,
                    'offsetCenter': [0, '70%'],
                    'fontSize': 30,
                    'fontWeight': 'bolder',
                    'formatter': '{value} °C',
                    'color': 'inherit'
                },
                'data': [
                    {'value': value,
                     'name': 'Temperature'}
                ]
            },
        ]
    }
    st_echarts(options=option)

def Humidity_chart(value):
    option = {
        'tooltip': {
            'formatter': '{b} : {c} %'
        },
        'series': [
            {
                'type': 'gauge',
                'center': ['50%', '60%'],
                'startAngle': 220,
                'endAngle': -40,
                # 'min': 0,
                # 'max': 40,
                'splitNumber': 10,
                'itemStyle': {
                    'color': '#FFAB91'
                },
                'progress': {
                    'show': True,
                    'width': 18
                },
                'axisLine': {
                    'lineStyle': {
                        'width': 18
                    }
                },
                # 刻度线的样式和行为
                'axisTick': {
                    'distance': -40,
                    'splitNumber': 5,
                    'lineStyle': {
                        'width': 2,
                        'color': '#999'
                    }
                },
                'splitLine': {
                    'distance': -46,
                    'length': 14,
                    'lineStyle': {
                        'width': 3,
                        'color': '#999'
                    }
                },
                'axisLabel': {
                    'distance': -20,
                    'color': '#999',
                    'fontSize': 20
                },
                'anchor': {
                    'show': True,
                    # 'showAbove': True,
                    # 'size': 25,
                    # 'itemStyle': {
                    #     'borderWidth': 10
                    # }
                },
                'title': {'show': True},
                'detail': {
                    'valueAnimation': True,
                    'fontSize': 30,
                    'offsetCenter': [0, '70%'],
                    'formatter': '{value} %',
                    'color': 'inherit'
                },
                'data': [
                    {
                        'value': value,
                        'name': 'Humidity'
                    }
                ]
            }
        ]
    }
    st_echarts(options=option)

def getData(datatype,location='',position='Window'):
    data = load_data()
    temperature_yes,temperature,humidity_yes,humidity = realTime(position)
    if datatype == 'location':
        list = ['Canteen', 'Library', 'Shop']
        return list
    elif datatype == 'position':
        return get_position(data)
    elif datatype == 'T':
        return temperature, temperature_yes
    elif datatype == 'H':
        return humidity,humidity_yes
    elif datatype == 'E':
        return Energy(location,position)

# 设置网页信息
st.set_page_config(page_title="FAU System Data Display", page_icon=":chart_increasing:📈", layout='centered')
# 页面布局
st.title('FAU System Data Display')  # 更改为自定义样式markdown语法
# st.markdown("<h1 style='text-align: center;'>FAU System Data Display</h1>", unsafe_allow_html=True)
# st.write('In this website, I\'ll make some pages to show different datas and charts collected by sensors.\n')
st.markdown('---')
# st.divider()
# 侧边栏 地点选择
list1 = getData('location')
location = ''
if list1:
    location = st.sidebar.selectbox(
        '# Choose Location',
        list1,
    )
else:
    st.write("error")
# st.sidebar 具体位置选择
list1 = getData('position')
position = ''
if list1:
    position = st.sidebar.selectbox(
        '# Choose Position',
        list1,
    )
    st.subheader('Temperature and humidity near ' + position + ' in ' + location)  # 更改为自定义样式markdown语法
    # st.markdown(f"<h3 style='text-align: center;'>Temperature and humidity near {option} in {location}</h3>", unsafe_allow_html=True)
else:
    st.write("error")


st.write('')
# 在streamlit中引入echarts, 插入温湿度表
t_today, t_last = getData('T',location,position)
# t_today = round(t_today, 2)
h_today, h_last = getData('H',location,position)
e_today, e_last = getData('E',location,position)
col1, col2 = st.columns(2)
with col1:
    Temperature_chart(t_today)
with col2:
    Humidity_chart(h_today)
# st.metric使用
''
st.write("### Temperature and Humidity compared with yesterday")  # 更改为自定义样式markdown语法
# st.markdown("\n<h3 style='text-align: center;'>Temperature, Humidity and Energy compared with yesterday</h3>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Temperature", str(t_today)+" °C", str(round(t_today-t_last,2))+" °C", delta_color="inverse")
col3.metric("Humidity", str(h_today)+"%", str(round(h_today-h_last,2))+"%", delta_color="inverse")
col5.metric("Energy", str(e_today)+" kWh", str(round(e_today-e_last,2))+" kWh", delta_color="inverse")
