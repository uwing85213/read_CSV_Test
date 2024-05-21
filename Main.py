import matplotlib.pyplot as plt
import csv
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

# with open("/content/drive/MyDrive/FN2_test/#1.csv", newline='') as csvfile:

  # 以冒號分隔欄位，讀取檔案內容
#   rows = csv.reader(csvfile, delimiter=':')
#   for row in rows:
    # print(row)



data = pd.read_csv("/content/drive/MyDrive/FN2_test/#1.csv")

len(data)

hearbit = data.iloc[:,58] #Heartbit data

plt.figure(figsize=(20,5))
plt.plot(hearbit, color='blue')


data_2 = data.iloc[:,49] #OGH_Bit data
#plt.figure(figsize=(20,5))
plt.plot(data_2, color='blue')


data_2 = data.iloc[:,17] #RPM data
data_3 = data.iloc[:,21] #RPM data
#plt.figure(figsize=(20,5))
plt.plot(data_2, color='blue')
plt.plot(data_3, color='red')


data_4 = data.iloc[:,3] #PL1 data
data_5 = data.iloc[:,8] #PL2 data
data_6 = data.iloc[:,13] #PL4 data
#plt.figure(figsize=(10,10))
plt.plot(data_4, color='blue' ,label='PL1')
plt.plot(data_5, color='red' ,label='PL2')
plt.plot(data_6, color='green',label='PL4')