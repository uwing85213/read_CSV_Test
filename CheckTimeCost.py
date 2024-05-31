import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import pandas as pd
import numpy as np
import codecs
from datetime import datetime, timedelta


def convert_to_24hr_format(time_str):
    """Convert a time string with '上午' or '下午' to 24-hour format."""
    time_str = time_str.strip()
    if "上午" in time_str:
        time_str = time_str.replace("上午", "AM")
    elif "下午" in time_str:
        time_str = time_str.replace("下午", "PM")
    try:
        return datetime.strptime(time_str, '%p %I:%M:%S')
    except ValueError:
        return datetime.strptime(time_str, '%H:%M:%S')

def calculate_time_difference(start_time, end_time):
    """Calculate the difference between two times and return as a formatted string."""
    start_dt = convert_to_24hr_format(start_time)
    end_dt = convert_to_24hr_format(end_time)
    
    # 如果 end_dt 小于 start_dt，说明跨过了午夜，添加一天时间
    if end_dt < start_dt:
        end_dt += timedelta(days=1)
    
    # 计算时间差
    time_diff = end_dt - start_dt
    
    # 提取小时、分钟和秒
    total_seconds = int(time_diff.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"总共花费 {hours}时 {minutes}分 {seconds}秒"



Time_Index = 0 # excel index : A

SaveDir_Path = "data/img/"


data = pd.read_csv("error_File/#8.csv")

Time_data = data.iloc[:,Time_Index]

# 原始时间字符串
a = Time_data[0]
b = Time_data.iloc[-1]

print(a)
print(b)
# 计算并输出时间差
time_difference_str = calculate_time_difference(a, b)
print(time_difference_str)