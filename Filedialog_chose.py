# -*- coding: utf-8 -*-
"""
Created on Tue May 21 22:47:52 2024

@author: YingRen
"""

import tkinter as tk
from tkinter import filedialog


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

root = tk.Tk()
root.withdraw()

directory = filedialog.askdirectory()