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
from datetime import datetime, timedelta
from natsort import natsorted

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
    csv_files = natsorted(csv_files)
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
def CombineImg(Path_img1,Path_img2,Path_img3,Path_img4,ImgSavePath,Sku_Name,Custom_Name=None):
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
    if Custom_Name == None:
        cv2.imwrite( (ImgSavePath + Sku_Name + '_combined.png'), combined_image)
    else:
        cv2.imwrite( (ImgSavePath + Sku_Name + Custom_Name), combined_image)
    # 圖片組合完成
    print(f"\n圖片組合完成!")

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
    end_dt   = convert_to_24hr_format(end_time)

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
    #return (f"\t,OGH經過: {hours}時 {minutes}分 {seconds}秒 就失聯, 時間: {hours}時 {minutes}分 {seconds}秒 \n")
    return (f"\t,OGH經過: {hours:02d}時 {minutes:02d}分 {seconds:02d}秒 就失聯, 時間: {hours:02d}時 {minutes:02d}分 {seconds:02d}秒 \n")

def calculate_time_Cost(Sec_Num):
    hours = Sec_Num // 3600
    minutes = (Sec_Num % 3600) // 60
    seconds = Sec_Num % 60
    return (f"\t,OGH經過: {hours:02d}時 {minutes:02d}分 {seconds:02d}秒 就失聯, 時間: {hours:02d}時 {minutes:02d}分 {seconds:02d}秒")

def Check_OGH_Bit_Diff(OGH_data, Time_data , FileTitle = None , bit0_Check_Error_Flag = False):
    # 初始化变量记录第一个变化的索引
    first_change_index = None
    time_difference_str = "0"
    diff_Flag = 0
    OGH_Mask_Bit = 0x1  # bit0
    data_len_error = False
    # print("type: ",type(OGH_data[0]),type(hex(OGH_data[0])))
    OGH_data_Index0_Dec = OGH_data[0]
    if bit0_Check_Error_Flag != True:
        OGH_data_Index0_Hex_bit0 = int(OGH_data[0]) & OGH_Mask_Bit
    else:
        OGH_data_Index0_Hex_bit0 = OGH_data[0]
    temp_Hex = 0x0
    if ( len(OGH_data) != len(Time_data)):
        data_len_error = True
        print("資料總長度不匹配")

    # 遍历列表
    for idx in range(1, len(OGH_data)):
        #檢查10進制是否不一樣
        if OGH_data[idx] != OGH_data_Index0_Dec and ( not np.isnan(OGH_data[idx]) ) :
            if bit0_Check_Error_Flag != True:   # 計算bit 0
                #檢查16進制,進一步檢查實際bit0
                temp_Hex = int(OGH_data[idx]) & OGH_Mask_Bit
                if temp_Hex != OGH_data_Index0_Hex_bit0 :
                    first_change_index = (idx+1)    # 從excel看要+1
            else: #不計算bit0
                first_change_index = (idx+1)    # 從excel看要+1
            print(OGH_data[idx] , OGH_data_Index0_Dec)
            break
    # 計算時間
    if first_change_index is not None:
        Start_time = Time_data[0]
        if (idx > len(Time_data)):
            print("長度不匹配,",idx,">",len(Time_data))
            diff_Flag = 2 # error
            time_difference_str = FileTitle + "_資料異常"
        else:
            print("Data index:",first_change_index)
            # End_time = Time_data[first_change_index] #算不出時間
            # End_time = Start_time + timedelta(seconds=first_change_index) # StartTime + (index * 1 sec)   不需要這個
            time_difference_str= calculate_time_Cost(first_change_index) # 直接計算花了幾秒就好
            time_difference_str = FileTitle + time_difference_str   # + sku name
            if bit0_Check_Error_Flag != True :
                time_difference_str +=" \n"
            else:
                time_difference_str += " ,無法針對bit 0計算,時間僅供參考 \n" 
        print(time_difference_str)
        diff_Flag = 1   #有可能異常
    else:
        print("沒有變化")
        diff_Flag = 0
    return diff_Flag , time_difference_str

# Parameter
Heartbit_Data_Index = 58 # excel index : BG
OGH_Bit_Data_Index = 49 # excel index : AX
Fan1_RPM_Index = 17 # excel index : R
Fan2_RPM_Index = 21 # excel index : V
Intel_PL4_Index = 13 # excel index : N
Intel_PL2_Index = 8 # excel index : I
Intel_PL1_Index = 3 # excel index : D
IR_temp_Index = 25  # for Round 46 , index : Z
CPU_temp_Index = 29 # for Round 46 , index : AD
VGA_temp_Index = 70 # for Round 46 , index : BS
Time_Index = 0 # excel index : A

figsize_setting = (9,7)
orange_color = "#DB6900"
puple_color  = '#9467BD' #深紫
green_color  = '#1EDB5A' #深綠
red_color    = '#DB3A82'
# 'blue'   = '#30C4DB'

# SaveDir_Path = "data/img/"
img_Path = "img/"
directory = ""
SaveDir_Path=""
# data = pd.read_csv("data/CSV_data/#3.csv")

Error_count = 0
Error_Flag=False
Error_string = ""
Str_buffer=""
TimeLog_Str=""
TimeLog_Flag = 0
TimeLog_buff = ""
Img_count=0

Img_Mix_Temp_RPM_Flag = 0

# 獲取當前工作目錄
current_working_directory = os.getcwd()

print("路徑盡量不要有中文\n")
print("============= Time Base: 一筆資料為 1 Sec =========\n")
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
        TimeLog_Flag = 0
        TimeLog_buff = ""
        Img_Mix_Temp_RPM_Flag = 0
        print(csv_file)
        HB_Img_Path = OGH_Img_Path = RPM_Img_Path = PLx_Img_Path = RPM_Img_Path2 = None
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

        # Read Time data
        try:
            Time_data = data.iloc[:,Time_Index]
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            Error_count+=1

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

            # 取bit0
            bit0_Check_Error_Flag = False
            try:
                OGH_Bit_Data_bit0 = [element & 0x1 for element in OGH_Bit_Data]
            except:
                bit0_Check_Error_Flag = True
                print("取bit0失敗,將改用原本Data")

            if (check_Colum_value == "OGH_Bit" ):
                plt.title(file_tile +"_Fan Ctrl")
                plt.grid(axis='y', linestyle='--')
                if bit0_Check_Error_Flag == True:
                    # oring data
                    if (np.nanmax(OGH_Bit_Data) >1) : # and (np.nanmin(OGH_Bit_Data) == 0)
                        plt.ylim(-0.1, 5.5) #ylabel = 0~6
                    else:   #有些檔案只有1跟0 我的天啊
                        plt.ylim(-0.1, 1.1) #ylabel = 0~6
                    plt.plot(OGH_Bit_Data, color='blue', label="Sku")
                else: # bit 0 data
                    plt.ylim(-0.1, 1.1) #ylabel = 0~6
                    plt.plot(OGH_Bit_Data_bit0, color='blue', label="Sku")
                
                
                plt.savefig(SaveDir_Path_new + file_tile +"_OGH.png", bbox_inches='tight', pad_inches=0.07)
                Img_count += 1
                OGH_Img_Path = (SaveDir_Path_new + file_tile +"_OGH.png")

                # 檢查時間差
                if bit0_Check_Error_Flag == True:
                    TimeLog_Flag , TimeLog_buff = Check_OGH_Bit_Diff( OGH_Bit_Data , Time_data , file_tile , bit0_Check_Error_Flag )
                else:
                    TimeLog_Flag , TimeLog_buff = Check_OGH_Bit_Diff( OGH_Bit_Data_bit0 , Time_data , file_tile , bit0_Check_Error_Flag )
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
                Img_Mix_Temp_RPM_Flag += 1  # 確認有圖
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
                plt.plot(Intel_PL4_data, color=red_color,label='PL4')
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
                plt.plot(VGA_temp_data, color=red_color ,label='VGA')
                plt.title( file_tile+ "_Temp")
                plt.legend() # loc='lower left'
                plt.savefig(SaveDir_Path_new + file_tile +"_Temp.png", bbox_inches='tight', pad_inches=0.07)
                Img_count += 1    # Temp不產圖，不計算
                Img_Mix_Temp_RPM_Flag += 1  # 確認有圖
            else:
                print(f"\n欄位index可能存在偏移 or 非10進位資料, 請手動產圖. 有問題的欄位為: {check_Colum_value},{check_Colum_value2},{check_Colum_value3} ,應是IR_Sensor,CPU_Temp,VGA_Temp \n")
                # Error_count+=1    # Temp其實沒差，有問題在處理
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            Error_count+=1
        
        # RPM mix Temp  For David

        try:
            if (Img_Mix_Temp_RPM_Flag >=2):
                plt.figure(figsize=figsize_setting)#, dpi=dpin
                plt.ylim(0, 101) #ylabel = 0~101
                plt.grid(axis='y', linestyle='--')

                plt.plot(IR_temp_data, color='blue',label='IR')
                plt.plot(CPU_temp_data, color=orange_color ,label='CPU')
                plt.plot(VGA_temp_data, color=red_color ,label='VGA')

                plt.plot(Fan1_RPM_data, color=green_color,label="Fan1_RPM" )
                plt.plot(Fan2_RPM_data, color=puple_color,label="Fan2_RPM")
                plt.title( file_tile+ "_RPM and Temp")

                plt.legend() # loc='lower left'
                plt.savefig(SaveDir_Path_new + file_tile +"_RPMandTemp.png", bbox_inches='tight', pad_inches=0.07)
                RPM_Img_Path2=(SaveDir_Path_new + file_tile +"_RPMandTemp.png")
            else:
                print(f"\n缺圖片無法做RPM + Temp的組合圖")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            # Error_count+=1

        # go to check index
        if TimeLog_Flag != 0:
            TimeLog_Str += TimeLog_buff
        # =======================================================
        if Img_count >= 4:
            if (HB_Img_Path != None) and (OGH_Img_Path != None) and (RPM_Img_Path != None) and (PLx_Img_Path != None) : #防止圖片路徑有問題
                # 輸出一般用的
                CombineImg(HB_Img_Path , OGH_Img_Path , RPM_Img_Path , PLx_Img_Path , SaveDir_Path_new , file_tile )
                # 額外再輸出一張
                if (Img_Mix_Temp_RPM_Flag >=2) and (RPM_Img_Path2 != None) : #輸出混合的
                    CombineImg(HB_Img_Path , OGH_Img_Path , RPM_Img_Path2 , PLx_Img_Path , SaveDir_Path_new , file_tile, Custom_Name = "_combined_Mix.png" )
                else:
                    print("無達成輸出混和的條件")
            else:
                print("有圖片產生錯誤!!")
                Error_count +=1 #代表有圖不見
        else:
            Error_count +=1
            print(f"\n不足4張圖,只有: {Img_count} 張")
        # =======================================================
        if Error_count >0:
            Error_string +="有問題的檔案:" + file_tile +"\n"
            Error_Flag=True
    # =======================================================
    if Error_Flag == True:
        with open( SaveDir_Path +'Error_Log.txt', 'w') as file:
            file.write(Error_string)
            file.write("\n欄位index可能存在偏移 or 非10進位資料, 請檢查資料夾內缺失的圖片,並手動產圖.")

    with open( SaveDir_Path +'OGH_Time_Log.txt', 'w') as file:
            file.write(TimeLog_Str)
            file.write("\n===========================")
            file.write("\n其他Sku沒有發現OGH Bit的變化")
    
else:
    print("No CSV file")
    

