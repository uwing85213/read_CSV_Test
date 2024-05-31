# -*- coding: utf-8 -*-
"""
Created on Tue May 21 22:54:41 2024

@author: YingRen
"""

import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import pandas as pd
import numpy as np
import codecs
import cv2

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
    # 定義預期的編碼列表，按優先順序排列
    expected_encodings = ['utf-8', 'cp950', 'big5', 'gb18030']  # 你也可以根據你的需求調整這個列表

    for encoding in expected_encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()  # 此處實際上不需要讀取文件內容，但是open函數會根據文件內容進行編碼檢測
                return encoding
        except UnicodeDecodeError:
            continue

    # 如果所有預期的編碼都失敗，則返回 None 或者引發異常，取決於你的需求
    return None

# 使用檢測到的編碼讀取 CSV 檔案
def read_csv_with_detected_encoding(file_path):
    encoding = detect_encoding(file_path)
    if encoding != None:
        print(f"Detected encoding: {encoding}")
        df = pd.read_csv(file_path, encoding=encoding, on_bad_lines='skip' )
        return df, True
    else:
        return None,False

# 去除非數值資料
def remove_non_numeric(df, column_index):
    # 選取特定的列並轉換為數值類型，非數值資料會被轉換為 NaN
    df.iloc[:, column_index] = pd.to_numeric(df.iloc[:, column_index], errors='coerce')
    # 去除包含 NaN 的行
    df = df.dropna(subset=[df.columns[column_index]])
    return df

# 自定义刻度格式化函数
def format_func(value, tick_number):
    return f'{value:.0f}'

# 
def CombineImg(Path_img1,Path_img2,Path_img3,Path_img4,ImgSavePath,Sku_Name):
    # HB_Img_Path , OGH_Img_Path , RPM_Img_Path , PLx_Img_Path 
    img1 = cv2.imread(Path_img1)
    img2 = cv2.imread(Path_img2)
    img3 = cv2.imread(Path_img3)
    img4 = cv2.imread(Path_img4)
    # print("shape_1:",img1.shape)
    # print("shape_2:",img2.shape)
    # print("shape_3:",img3.shape)
    # print("shape_4:",img4.shape)
    height, width, _ = img1.shape
    # img1 = cv2.resize(img1, (width, height))
    img2 = cv2.resize(img2, (width, height))
    img3 = cv2.resize(img3, (width, height))
    img4 = cv2.resize(img4, (width, height))

    # 組合左上和右上圖片
    top_row = np.hstack((img4, img2))
    # 組合左下和右下圖片
    bottom_row = np.hstack((img1, img3))
    # 將上下兩行圖片組合起來
    combined_image = np.vstack((top_row, bottom_row))
    # 保存組合後的圖片
    cv2.imwrite( (ImgSavePath + Sku_Name + '_combined.png'), combined_image)
    # 圖片組合完成
    print(f"\n圖片組合完成!")

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

Error_count = 0
Error_Flag=False
Error_string = ""
Str_buffer=""
Img_count=0

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
    Error_string = ""
    Error_Flag = False
    for csv_file in csv_files:
        Error_count = 0
        Img_count = 0
        print(csv_file)
        # do
        file_tile = csv_file.split('/')[-1][:-4]
        
        # SaveDir_Path += file_tile

        create_or_check_directory(SaveDir_Path + file_tile + "/" )
        SaveDir_Path_new =  SaveDir_Path + file_tile + "/"

        # data = pd.read_csv( csv_file )
        data, flag = read_csv_with_detected_encoding( csv_file )

        if flag == False:
            Error_count+=1
            continue

        try:
            plt.figure(figsize=figsize_setting)#, dpi=dpin
            Heartbit_data = data.iloc[:,Heartbit_Data_Index] #Heartbit data
            check_Colum_value = data.iloc[ 0 , Heartbit_Data_Index-3]
            if (check_Colum_value == "Heartbit" ):
                plt.ylim(-10, 1400) #ylabel = 0~6
                plt.grid(axis='y', linestyle='--',color='gray', linewidth=1)
                plt.plot(Heartbit_data, color='blue',linestyle='-', label="Heartbit")
                plt.title(file_tile + "_Heartbit")
                plt.savefig(SaveDir_Path_new + file_tile +"_HB.png", bbox_inches='tight', pad_inches=0.07)
                HB_Img_Path = (SaveDir_Path_new + file_tile +"_HB.png")
                Img_count += 1
            else:
                print(f"\n欄位index可能存在偏移 or 非10進位資料, 請手動產圖. 有問題的欄位為: {check_Colum_value},應是Heartbit \n")
                Error_count+=1
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            Error_count+=1

        try:
            plt.figure(figsize=figsize_setting) 
            OGH_Bit_Data = data.iloc[:,OGH_Bit_Data_Index] #OGH_Bit data
            check_Colum_value = data.iloc[ 0 , OGH_Bit_Data_Index-2]
            if (check_Colum_value == "OGH_Bit" ):
                plt.ylim(-0.1, 6) #ylabel = 0~6
                plt.grid(axis='y', linestyle='--')
                plt.plot(OGH_Bit_Data, color='blue', label="Sku")
                plt.title(file_tile +"_Fan Ctrl")
                plt.savefig(SaveDir_Path_new + file_tile +"_OGH.png", bbox_inches='tight', pad_inches=0.07)
                Img_count += 1
                OGH_Img_Path = (SaveDir_Path_new + file_tile +"_OGH.png")
            else:
                print(f"\n欄位index可能存在偏移 or 非10進位資料, 請手動產圖. 有問題的欄位為: {check_Colum_value},應是OGH_Bit \n")
                Error_count+=1
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            Error_count+=1

        try:
            plt.figure(figsize=figsize_setting)#, dpi=dpin
            Fan1_RPM_data = data.iloc[:,Fan1_RPM_Index] #RPM data
            Fan2_RPM_data = data.iloc[:,Fan2_RPM_Index] #RPM data
            check_Colum_value = data.iloc[ 0 , Fan1_RPM_Index-2]
            check_Colum_value2 = data.iloc[ 0 , Fan2_RPM_Index-2]
            if (check_Colum_value == "FAN1_RPM" and check_Colum_value2 == "FAN2_RPM" ):
                plt.ylim(0, 70) #ylabel = 0~70
                plt.grid(axis='y', linestyle='--')
                plt.plot(Fan1_RPM_data, color='blue',label="Fan1_RPM" )
                plt.plot(Fan2_RPM_data, color=orange_color,label="Fan2_RPM")
                plt.title(file_tile + "_FAN RPM")
                plt.legend()
                plt.savefig(SaveDir_Path_new + file_tile +"_RPM.png", bbox_inches='tight', pad_inches=0.07)
                Img_count += 1
                RPM_Img_Path = (SaveDir_Path_new + file_tile +"_RPM.png")
            else:
                print(f"\n欄位index可能存在偏移 or 非10進位資料, 請手動產圖. 有問題的欄位為: {check_Colum_value},應是FAN1_RPM,FAN2_RPM \n")
                Error_count+=1

        except Exception as e:
            print(f"\nAn error occurred: {e}")
            Error_count+=1

        try:
            plt.figure(figsize=figsize_setting)#, dpi=dpin
            Intel_PL1_data = data.iloc[:,Intel_PL1_Index] #PL1 data
            Intel_PL2_data = data.iloc[:,Intel_PL2_Index] #PL2 data
            Intel_PL4_data = data.iloc[:,Intel_PL4_Index] #PL4 data
            check_Colum_value = data.iloc[ 0 , Intel_PL1_Index-2]
            check_Colum_value2 = data.iloc[ 0 , Intel_PL2_Index-3]
            check_Colum_value3 = data.iloc[ 0 , Intel_PL4_Index-3]
            if (check_Colum_value == "PL1" and check_Colum_value2 == "PL2" and check_Colum_value3 == "PL4" ):
                plt.ylim(-1, 250) #ylabel = 0~6
                plt.grid(axis='y', linestyle='--')
                plt.plot(Intel_PL4_data, color='gray',label='PL4')
                plt.plot(Intel_PL1_data, color='blue' ,label='PL1')
                plt.plot(Intel_PL2_data, color=orange_color ,label='PL2')
                plt.title(file_tile + "_PLx")
                plt.legend()
                plt.savefig(SaveDir_Path_new + file_tile +"_PLx.png", bbox_inches='tight', pad_inches=0.07)
                Img_count += 1
                PLx_Img_Path = (SaveDir_Path_new + file_tile +"_PLx.png")
            else:
                print(f"\n欄位index可能存在偏移 or 非10進位資料, 請手動產圖. 有問題的欄位為: {check_Colum_value},{check_Colum_value2},{check_Colum_value3} ,應是PL1,PL2,PL4 \n")
                Error_count+=1
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            Error_count+=1

        try:
            plt.figure(figsize=figsize_setting)#, dpi=dpin
            IR_temp_data = data.iloc[:,IR_temp_Index] #PL1 data
            CPU_temp_data = data.iloc[:,CPU_temp_Index] #PL2 data
            VGA_temp_data = data.iloc[:,VGA_temp_Index] #PL4 data
            check_Colum_value = data.iloc[ 0 , IR_temp_Index-2]
            check_Colum_value2 = data.iloc[ 0 , CPU_temp_Index-2]
            check_Colum_value3 = data.iloc[ 0 , VGA_temp_Index-2]
            if (check_Colum_value == "IR_Sensor" and check_Colum_value2 == "CPU_Temp" and check_Colum_value3 == "VGA_Temp" ):
                plt.ylim(-1, 101) #ylabel = 0~6
                plt.grid(axis='y', linestyle='--')
                plt.plot(IR_temp_data, color='blue',label='IR')
                plt.plot(CPU_temp_data, color=orange_color ,label='CPU')
                plt.plot(VGA_temp_data, color='gray' ,label='VGA')
                plt.title( file_tile+ "_Temp")
                plt.legend() # loc='lower left'
                plt.savefig(SaveDir_Path_new + file_tile +"_Temp.png", bbox_inches='tight', pad_inches=0.07)
                # Img_count += 1    # Temp不產圖，不計算
            else:
                print(f"\n欄位index可能存在偏移 or 非10進位資料, 請手動產圖. 有問題的欄位為: {check_Colum_value},{check_Colum_value2},{check_Colum_value3} ,應是IR_Sensor,CPU_Temp,VGA_Temp \n")
                # Error_count+=1    # Temp其實沒差，有問題在處理
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            Error_count+=1

        if Error_count >0:
            Error_string +="有問題的檔案:" + file_tile +"\n"
            Error_Flag=True
        # =======================================================
        if Img_count >= 4:
            CombineImg(HB_Img_Path , OGH_Img_Path , RPM_Img_Path , PLx_Img_Path , SaveDir_Path_new , file_tile )
        else:
            print(f"\n不足4張圖,只有: {Img_count} 張")
    # =======================================================
    if Error_Flag == True:
        with open( SaveDir_Path +'Error_Log.txt', 'w') as file:
            file.write(Error_string)
            file.write("\n欄位index可能存在偏移 or 非10進位資料, 請手動產圖.")
    
else:
    print("No CSV file")
    

