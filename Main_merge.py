# -*- coding: utf-8 -*-
"""
Created on Tue May 21 22:54:41 2024

@author: YingRen
"""

import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
import chardet

def find_csv_files(directory):
    """
    搜尋指定資料夾內的所有 CSV 檔案。

    參數:
    directory (str): 要搜尋的資料夾路徑。

    返回:
    list: CSV 檔案的完整路徑列表。
    """
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

def create_or_check_directory(directory):
    """
    判斷資料夾是否存在，如果不存在則建立之。

    參數:
    directory (str): 要檢查或建立的資料夾路徑。
    """
    if not os.path.exists(directory):
        # 如果資料夾不存在，則建立之
        os.makedirs(directory)
        print(f"資料夾 '{directory}' 建立成功")
    else:
        print(f"資料夾 '{directory}' 已經存在")

# 檢測檔案編碼
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding

# 使用檢測到的編碼讀取 CSV 檔案
def read_csv_with_detected_encoding(file_path):
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")
    df = pd.read_csv(file_path, encoding=encoding)
    return df


# Parameter
Heartbit_Data_Index = 58
OGH_Bit_Data_Index = 49
Fan1_RPM_Index = 17
Fan2_RPM_Index = 21
Intel_PL4_Index = 13
Intel_PL2_Index = 8
Intel_PL1_Index = 3
IR_temp_Index = 25
CPU_temp_Index = 29
VGA_temp_Index = 78

figsize_setting = (9,7)
orange_color= "#EA6E1A"

# SaveDir_Path = "data/img/"
img_Path = "img/"
directory = ""
SaveDir_Path=""
# data = pd.read_csv("data/CSV_data/#3.csv")

# 獲取當前工作目錄
current_working_directory = os.getcwd()

print("Chose csv root path :")
root_tk = tk.Tk()
root_tk.withdraw()
directory_path = filedialog.askdirectory(initialdir=current_working_directory, title="選擇有CSV的資料夾")
directory_path+="/"

csv_files = find_csv_files(directory_path )

if len(csv_files) >0 :
    create_or_check_directory(directory_path + img_Path)
    # 搜檔案
    SaveDir_Path = directory_path + img_Path
    for csv_file in csv_files:
        print(csv_file)
        
        # do
        file_tile = csv_file.split('/')[-1][:-4]
        
        # SaveDir_Path += file_tile

        create_or_check_directory(SaveDir_Path + file_tile + "/" )
        SaveDir_Path_new =  SaveDir_Path + file_tile + "/"

        # data = pd.read_csv( csv_file )
        data = read_csv_with_detected_encoding( csv_file )
        
        plt.figure(figsize=figsize_setting)#, dpi=dpin
        Heartbit_data = data.iloc[:,Heartbit_Data_Index] #Heartbit data
        plt.plot(Heartbit_data, color='blue',linestyle='-', label="Heartbit")
        plt.title("Heartbit")
        plt.savefig(SaveDir_Path_new + file_tile +"_HB.png")

        plt.figure(figsize=figsize_setting) 
        data_2 = data.iloc[:,OGH_Bit_Data_Index] #OGH_Bit data
        plt.plot(data_2, color='blue', label="Sku")
        plt.title("Fan Ctrl")
        plt.savefig(SaveDir_Path_new + file_tile +"_OGH.png")

        plt.figure(figsize=figsize_setting)#, dpi=dpin
        Fan1_RPM_data = data.iloc[:,Fan1_RPM_Index] #RPM data
        Fan2_RPM_data = data.iloc[:,Fan2_RPM_Index] #RPM data
        plt.plot(Fan1_RPM_data, color='blue',label="Fan1_RPM" )
        plt.plot(Fan2_RPM_data, color=orange_color,label="Fan2_RPM")
        plt.title("FAN RPM")
        plt.legend()
        plt.savefig(SaveDir_Path_new + file_tile +"_RPM.png")

        plt.figure(figsize=figsize_setting)#, dpi=dpin
        Intel_PL1_data = data.iloc[:,Intel_PL1_Index] #PL1 data
        Intel_PL2_data = data.iloc[:,Intel_PL2_Index] #PL2 data
        Intel_PL4_data = data.iloc[:,Intel_PL4_Index] #PL4 data
        plt.plot(Intel_PL4_data, color='gray',label='PL4')
        plt.plot(Intel_PL1_data, color='blue' ,label='PL1')
        plt.plot(Intel_PL2_data, color=orange_color ,label='PL2')
        plt.title(file_tile)
        plt.legend()
        plt.savefig(SaveDir_Path_new + file_tile +"_PLx.png")

        plt.figure(figsize=figsize_setting)#, dpi=dpin
        IR_temp_data = data.iloc[:,IR_temp_Index] #PL1 data
        CPU_temp_data = data.iloc[:,CPU_temp_Index] #PL2 data
        VGA_temp_data = data.iloc[:,VGA_temp_Index] #PL4 data
        plt.plot(IR_temp_data, color='blue',label='IR')
        plt.plot(CPU_temp_data, color=orange_color ,label='CPU')
        plt.plot(VGA_temp_data, color='gray' ,label='VGA')
        plt.title("Temp")
        plt.legend() # loc='lower left'
        plt.savefig(SaveDir_Path_new + file_tile +"_Temp.png")
    
else:
    print("No CSV file")
    

