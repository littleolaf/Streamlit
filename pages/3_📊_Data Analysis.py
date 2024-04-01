import numpy as np
import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts
from datetime import datetime, date

# 设置网页信息
st.set_page_config(page_title="FAU System Data Display", page_icon=":chart_increasing:📈", layout='wide')

from pages.data.load_data import load_data, meanMonth, meanWeek, peakTime, powerBar, get_position

# 设置网页标题
# st.title("Data Analysis Display")  # 更改为自定义样式markdown语法
st.markdown(f"<h1 style='text-align: center;'>Data Analysis Display</h1>", unsafe_allow_html=True)
# 获取数据帧
data = load_data()

# 设置expander,展示每月平均温湿度
with st.expander('Month Average Temperature & Humidity'):
    # st.write('FAU off')
    list1 = get_position(data)
    position = st.selectbox(
        '# Choose Position',
        list1,
        key='month position'
    )
    st.subheader('Temperature and humidity near ' + position)  # 更改为自定义样式markdown语法
    # st.markdown(f"<h3 style='text-align: center;'>Temperature and humidity near {option} in {location}</h3>", unsafe_allow_html=True)

    months, temperature, humidity = meanMonth(data, position)
    option = {
        # 鼠标悬浮图释,悬浮窗
        'tooltip': {},
        # 图例
        'legend': {},
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
                'end': 100,
                # 'xAxisIndex': [0, 1]
            },
            {
                'type': 'inside',
                'realtime': True,
            }
        ],
        'xAxis': {
            'name': 'Month',
            'type': 'category',
            'data': months
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
                'data': humidity,
                'type': 'bar',
                'smooth': True,
                'label': {
                    'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} %'
                }
            },
            {
                'name': 'Temperature',
                'data': temperature,
                'type': 'bar',
                'smooth': True,
                'label': {
                    'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} °C'
                }
            }
        ]
    }
    st_echarts(options=option, key='month_chart')
# 设置expander,展示每周平均温湿度
with st.expander('Week Average Temperature & Humidity'):
    list1 = get_position(data)
    position = st.selectbox(
        '# Choose Position',
        list1,
        key='week position'
    )
    st.subheader('Temperature and humidity near ' + position)  # 更改为自定义样式markdown语法
    # st.markdown(f"<h3 style='text-align: center;'>Temperature and humidity near {option} in {location}</h3>", unsafe_allow_html=True)
    # 获取图表数据
    weeks, temperature, humidity = meanWeek(data, position)
    option = {
        # 鼠标悬浮图释,悬浮窗
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'  #type：指示器类型。可以选择的类型包括：'line'：直线指示器。'shadow'：阴影指示器，用于在柱状图或折线图中显示阴影区域。'cross'：十字准星指示器，可以同时显示横轴和纵轴上的标记线。
            }
        },
        # 图例
        'legend': {},
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
                'end': 100,
                'filterMode': 'filter'
            },
            {
                'type': 'inside',
                'realtime': True,
            }
        ],
        'xAxis': {
            'name': 'Weeks',
            'type': 'category',
            'data': weeks,
            'boundaryGap': False  # 设置 boundaryGap 为 false,让折线图值落在x刻度上
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
                'data': humidity,
                'type': 'line',
                'smooth': True,
                'label': {
                    'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} %'
                }
            },
            {
                'name': 'Temperature',
                'data': temperature,
                'type': 'line',
                'smooth': True,
                'label': {
                    'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} °C'
                }
            }
        ]
    }
    st_echarts(options=option, key='week_chart')
# 设置expander,展示高峰时刻（中晚），FAU on/off的温湿度
with st.expander('Peak Time Average Temperature & Humidity'):
    list1 = get_position(data)
    position = st.selectbox(
        '# Choose Position',
        list1,
        key='peak_time position'
    )
    peak_time = st.selectbox(
        '# Choose Time',
        ['lunch', 'dinner'],
        key='meal time'
    )
    st.subheader('Temperature and humidity near ' + position + ' at '+peak_time)  # 更改为自定义样式markdown语法
    # st.markdown(f"<h3 style='text-align: center;'>Temperature and humidity near {option} in {location}</h3>", unsafe_allow_html=True)
    days, temperature_on, humidity_on, temperature_off, humidity_off = peakTime(data,position,peak_time)
    # days, temperature_on, humidity_on, temperature_off, humidity_off
    option = {
        # 鼠标悬浮图释,悬浮窗
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
                # type：指示器类型。可以选择的类型包括：'line'：直线指示器。'shadow'：阴影指示器，用于在柱状图或折线图中显示阴影区域。'cross'：十字准星指示器，可以同时显示横轴和纵轴上的标记线。
            }
        },
        # 图例
        'legend': {},
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
        # 对齐x轴
        'axisPointer': {
            'link': [
                {
                    'xAxisIndex': 'all'
                }
            ]
        },
        # 数据选区范围工具
        'dataZoom': [
            {
                'show': True,
                'type': 'inside',
                'realtime': True,
                'start': 0,
                'end': 100,
                'xAxisIndex': [0, 1]
            }
        ],
        'grid': [
            {
              # 'left': 30,
              # 'right': 30,
              'height': '35%'
            },
            {
                # 'left': 30,
                # 'right': 30,
                'top': '55%',
                'height': '35%'
            }
        ],
        'xAxis': [
            {
                'name': 'Weeks',
                'type': 'category',
                'data': days,
                'boundaryGap': False  # 设置 boundaryGap 为 false,让折线图值落在x刻度上
            },
            {
                'gridIndex': 1,
                'name': 'Weeks',
                'type': 'category',
                'data': days,
                'boundaryGap': False,  # 设置 boundaryGap 为 false,让折线图值落在x刻度上
                'position': 'top'
            }
        ],
        # 双y轴
        'yAxis': [
            {
                'name': 'Temperature(°C)',
                'type': 'value'
            },
            {
                'gridIndex': 1,  # 将y轴放在第二幅图中
                'name': 'Humidity(%)',
                'type': 'value',
                'inverse': True  # 颠倒y轴
            }

        ],
        'series': [
            {
                'name': 'Humidity(FAU ON)',
                'data': humidity_on,
                'type': 'line',
                # 'smooth': True,
                'yAxisIndex': 1,
                'xAxisIndex': 1,
                'connectNulls': True,  # 设置为 true，使得折线图能够连接缺失值
                'label': {
                    # 'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} %'
                }
            },
            {
                'name': 'Temperature(FAU ON)',
                'data': temperature_on,
                'type': 'line',
                # 'smooth': True,
                'connectNulls': True,  # 设置为 true，使得折线图能够连接缺失值
                'label': {
                    # 'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} °C'
                }
            },
            {
                'name': 'Humidity(FAU OFF)',
                'data': humidity_off,
                'type': 'line',
                # 'smooth': True,
                'yAxisIndex': 1,
                'xAxisIndex': 1,
                'connectNulls': True,  # 设置为 true，使得折线图能够连接缺失值
                'label': {
                    # 'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} %'
                }
            },
            {
                'name': 'Temperature(FAU OFF)',
                'data': temperature_off,
                'type': 'line',
                # 'smooth': True,
                'connectNulls': True,  # 设置为 true，使得折线图能够连接缺失值
                'label': {
                    # 'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} °C'
                }
            }
        ]
    }
    st_echarts(options=option, key='peak_chart')
# 设置expander,展示能源消耗对比柱状图 todo:pie图的数据是人为写死的
with st.expander('Total Energy Consumption in recent Years'):
    month, year2018, year2019, year2023, FAU = powerBar()
    total2023 = np.add(year2023, FAU)
    option1 = {
        'title': {
            'text': 'Canteen Cooling Power Consumption'
        },
        # 鼠标悬浮图释,悬浮窗
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'shadow'
                # type：指示器类型。可以选择的类型包括：'line'：直线指示器。'shadow'：阴影指示器，用于在柱状图或折线图中显示阴影区域。'cross'：十字准星指示器，可以同时显示横轴和纵轴上的标记线。
            }
        },
        # 图例
        'legend': {},
        # 右上角工具栏
        'toolbox': {
            'show': True,
            'feature': {
                'dataZoom': {
                    'yAxisIndex': 'none'
                },
                # 'dataView': {'readOnly': False},
                # 'magicType': {'type': ['line', 'bar']},
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
                'end': 100,
                'filterMode': 'filter',
                'xAxisIndex': [0, 1]
            },
            {
                'type': 'inside',
                'realtime': True,
                'xAxisIndex': [0, 1]
            }
        ],
        'xAxis': [
            {
                'name': 'Months',
                'type': 'category',
                'data': month,
                # 'boundaryGap': False  # 设置 boundaryGap 为 false,让折线图值落在x刻度上
            }
        ],
        # y轴
        'yAxis': [
            {
                'name': 'Power(kWh)',
                'type': 'value'
            }
        ],
        'series': [
            {
                'name': 'Year 2018',
                'data': year2018,
                'type': 'bar',
                'stack': '2018',
                # 'smooth': True,
                # 'connectNulls': True,  # 设置为 true，使得折线图能够连接缺失值
                'label': {
                    'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} kWh'
                },
                'emphasis': {'focus': 'series'}
            },
            {
                'name': 'Year 2019',
                'data': year2019,
                'type': 'bar',
                'stack': '2019',
                # 'smooth': True,
                # 'connectNulls': True,  # 设置为 true，使得折线图能够连接缺失值
                'label': {
                    'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} kWh'
                },
                'emphasis': {'focus': 'series'}
            },
            {
                'name': 'Year 2023',
                'data': year2023,
                'type': 'bar',
                'stack': '2023',
                # 'smooth': True,
                # 'connectNulls': True,  # 设置为 true，使得折线图能够连接缺失值
                'label': {
                    'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} kWh'
                },
                'emphasis': {'focus': 'series'}
            },
            {
                'name': 'FAU Consumption',
                'data': FAU,
                'type': 'bar',
                'stack': '2023',
                # 'smooth': True,
                # 'connectNulls': True,  # 设置为 true，使得折线图能够连接缺失值
                'label': {
                    'show': True,  # 显示数值
                    'position': 'top',  # 数值显示在柱状图顶端
                    'formatter': '{c} kWh',
                },
                'emphasis': {'focus': 'series'}
            }
        ]
    }
    st_echarts(options=option1, key='energy_barchart')
    option2 = {
        'title': {
            'text': 'Saved Energy Compared with 2019 (8-June to 30-June)'
        },
        # 悬浮解释框
        'tooltip': {
            'trigger': 'item'
        },
        # 图例
        'legend': {
            # 'orient': 'vertical',
            'top': 'bottom'
        },
        'series': [
            {
                'selectedMode': 'single',
                'type': 'pie',
                'data': [
                    {'value': 15522.75 / 27774.23,  'name': 'Air Conditioner'},
                    {'value':  5771.25 / 27774.23, 'name': 'FAU'},
                    {'value': 0.2333, 'name': 'Saved', 'selected': 'true'}
                ],
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                },
                'label': {
                    'show': True,
                    'formatter': '{b} : {d} %'  # 显示名称和占比
                }
            }
        ]
    }
    st_echarts(options=option2, key='energy_piechart')
