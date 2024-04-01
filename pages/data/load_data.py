import streamlit as st
import pandas as pd
import datetime


@st.cache_data  # 将数据缓存至网页上，加速后续刷新网页的加载速度
def load_data():
    data = pd.read_excel('./Summary V2.xlsx')  # , sheet_name=['18-May to 26-June', '26-June to 19-Sep']
    sheet2 = pd.read_excel('./Summary V2.xlsx', sheet_name="26-June to 19-Sep")
    data = pd.concat([data, sheet2], ignore_index=True)  # 忽略索引确保后续添加的索引正确连续
    data["Humidity"] = pd.to_datetime(data["Humidity"], dayfirst=True)  # , format="%d/%m/%Y %H:%M:%S"
    empty_cols = [col for col in data.columns if data[col].isnull().all()]
    data.drop(empty_cols, axis=1, inplace=True)
    # st.line_chart(data)
    return data
# 每月平均温湿度
def meanMonth(data,position):
    temperature = []
    humidity = []
    months = []
    start_day = data["Humidity"][0].replace(hour=0, minute=0, second=0)  # 第一天,只保留年月日
    start_month = start_day + pd.offsets.MonthBegin(n=-1)  # 移动到当前月第一天
    # st.write(start_day,start_month)
    end_day = data["Humidity"].iloc[-1].replace(hour=0, minute=0, second=0)  # 记录的最后一天
    while start_month < end_day:
        month_end = start_month + pd.offsets.MonthBegin(n=1)
        df = data[(data["Humidity"] > start_month) & (data["Humidity"] < month_end)]  # 获取这一月内的所有数据
        temperature.append(round(df[position + '.1'].mean(), 2))
        humidity.append(round(df[position].mean(), 2))
        months.append(start_month.strftime('%Y-%m'))  # str(start_month.year)+'-'+str(start_month.month)
        start_month = month_end
        pass
    # st.write(months,temperature,humidity)
    return months,temperature,humidity
# 每周平均温湿度
def meanWeek(data,position):
    temperature = []
    humidity = []
    weeks = []
    first_date = data["Humidity"][0].replace(hour=0, minute=0, second=0)  # 第一天,只保留年月日
    start_week = first_date + pd.DateOffset(weeks=-1, weekday=0)  # 将起始记录挪到这周的周一
    end_date = data["Humidity"].iloc[-1]  # 记录里最后一天数据
    # st.write(end_date)
    # first_weekday = data["Humidity"][0].weekday()  # 判断记录里第一周是周几
    while start_week < end_date:
        week_end = start_week + pd.DateOffset(weeks=1,weekday=0)  # 下一周周一0点为界
        df = data[(data["Humidity"] > start_week) & (data["Humidity"] < week_end)]  # 获取这一周内的所有数据
        temperature.append(round(df[position + '.1'].mean(), 2))
        humidity.append(round(df[position].mean(), 2))
        weeks.append(start_week.strftime('%Y-%m-%d'))  # str(start_week.year)+'-'+str(start_week.month)+'-'+str(start_week.day)
        start_week = week_end  # 将起始日期移至下周一
        pass
    return weeks, temperature, humidity
# 每日高峰时刻，fau on/off的温湿度对比。1.区分fau on/off的日期 8/6/2023 2.分别求每日高峰时刻的平均温湿度
def peakTime(data,position,time=''):
    temperature_on = []
    humidity_on = []
    temperature_off = []
    humidity_off = []
    days = []
    peak_time = datetime.timedelta(hours=12)
    # peak_time = pd.DateOffset(hours=12)
    if time == 'dinner':
        peak_time = datetime.timedelta(hours=18)
        # peak_time = pd.DateOffset(hours=18)
    first_date = data["Humidity"][0].replace(hour=0, minute=0, second=0)  # 第一天,只保留年月日
    end_date = data["Humidity"].iloc[-1]  # 记录里最后一天数据
    while first_date < end_date:
        start_time = first_date + peak_time
        end_time = start_time + datetime.timedelta(hours=2, minutes=30)
        df = data[(data["Humidity"] > start_time) & (data["Humidity"] < end_time)]  # 获取本日该高峰期内所有数据
        days.append(first_date.strftime('%Y-%m-%d'))
        if df.empty:  # 判断是否有数据
            temperature_off.append(None)
            humidity_off.append(None)
            temperature_on.append(None)
            humidity_on.append(None)
            pass
        else:
            # 判断该日FAU系统是否开启
            if (start_time < pd.to_datetime('9/06/2023', dayfirst=True)) | (start_time.weekday() == 6):  # 未开启fau系统的日子
                temperature_off.append(round(df[position + '.1'].mean(), 2))
                humidity_off.append(round(df[position].mean(), 2))
                temperature_on.append(None)
                humidity_on.append(None)
            else:
                temperature_on.append(round(df[position + '.1'].mean(), 2))
                humidity_on.append(round(df[position].mean(), 2))
                temperature_off.append(None)
                humidity_off.append(None)
                pass
        first_date = first_date + pd.DateOffset(days=1)  # 将日期向后顺延一天
        pass

    return days,temperature_on,humidity_on,temperature_off,humidity_off

def powerBar():
    month = ['8-June to 30-June', 'July', 'August']
    year2018 = [23770.99, 34567.07, 35105.91]
    year2019 = [27774.23, 38079.93, 36507.09]
    year2023 = [15522.75, 23243.18, 29825.45]
    FAU = [5771.25, 6628.23, 6999.25]
    size_june = [15522.75 / 27774.23, 5771.25 / 27774.23, 0.2333]
    size_july = [23243.18 / 38079.93, 6628.23 / 38079.93, 0.2156]
    return month,year2018,year2019,year2023,FAU

def realTime(position):
    data = load_data()
    today = data["Humidity"].iloc[-1].replace(hour=0, minute=0, second=0)  # 记录里最新的数据
    yesterday = today + pd.DateOffset(days=-1)
    temperature = round(data[position+'.1'].iloc[-1],2)
    humidity = round(data[position].iloc[-1],2)
    df = data[(data["Humidity"] > yesterday) & (data["Humidity"] < today)]  # 获取昨天的所有数据
    temperature_yes = round(df[position+'.1'].mean(),2)
    humidity_yes = round(df[position].mean(),2)
    return temperature_yes,temperature,humidity_yes,humidity
def get_position(data):
    # todo:未真正自动提取地点值
    column_list = data.columns.tolist()
    column_list = [name for name in column_list if name is not None]  # todo 列名称筛选以获取地点名称
    list1 = ["Window", "Near Lounge", "Near Harmony"]
    return list1  # column_list
