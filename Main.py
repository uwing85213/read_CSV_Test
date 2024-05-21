import matplotlib.pyplot as plt
import csv
import pandas as pd

# from google.colab import drive
# drive.mount('/content/drive')

# with open("/content/drive/MyDrive/FN2_test/#1.csv", newline='') as csvfile:

  # 以冒號分隔欄位，讀取檔案內容
#   rows = csv.reader(csvfile, delimiter=':')
#   for row in rows:
    # print(row)

# Parameter
Heartbit_Data_Index = 58

OGH_Bit_Data_Index = 49

Fan1_RPM_Index = 17
Fan2_RPM_Index = 21

Intel_PL4_Index = 13
Intel_PL2_Index = 8
Intel_PL1_Index = 3


SaveDir_Path = "data/img/"

figsize_setting = (7,5)


data = pd.read_csv("data/CSV_data/#3.csv")

plt.figure(figsize=figsize_setting)#, dpi=dpin
Heartbit_data = data.iloc[:,Heartbit_Data_Index] #Heartbit data
plt.plot(Heartbit_data, color='blue',linestyle='-', label="Heartbit")
plt.title("Heartbit")
plt.savefig(SaveDir_Path+"_HB.png")

plt.figure(figsize=figsize_setting) 
data_2 = data.iloc[:,OGH_Bit_Data_Index] #OGH_Bit data
plt.plot(data_2, color='blue', label="Sku")
plt.title("Fan Ctrl")
plt.savefig(SaveDir_Path+"_OGH.png")

plt.figure(figsize=figsize_setting)#, dpi=dpin
Fan1_RPM_data = data.iloc[:,Fan1_RPM_Index] #RPM data
Fan2_RPM_data = data.iloc[:,Fan2_RPM_Index] #RPM data
plt.plot(Fan1_RPM_data, color='blue',label="Fan1_RPM" )
plt.plot(Fan2_RPM_data, color='orange',label="Fan2_RPM")
plt.title("FAN RPM")
plt.legend()
plt.savefig(SaveDir_Path+"_RPM.png")

plt.figure(figsize=figsize_setting)#, dpi=dpin
Intel_PL1_data = data.iloc[:,Intel_PL1_Index] #PL1 data
Intel_PL2_data = data.iloc[:,Intel_PL2_Index] #PL2 data
Intel_PL4_data = data.iloc[:,Intel_PL4_Index] #PL4 data
plt.plot(Intel_PL4_data, color='gray',label='PL4')
plt.plot(Intel_PL2_data, color='orange' ,label='PL2')
plt.plot(Intel_PL1_data, color='blue' ,label='PL1')
plt.title("Sku name")
plt.legend()
plt.savefig(SaveDir_Path+"_PLx.png")