# -*- coding: utf-8 -*-
"""
Created on Tue May 21 22:00:30 2024

@author: YingRen
"""

import os
import tkinter as tk

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

# 使用範例
directory_path = 'data/CSV_data/'  # 請替換成你要搜尋的資料夾路徑
csv_files = find_csv_files(directory_path)

for csv_file in csv_files:
    a = csv_file
    print(csv_file)
    
