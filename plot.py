import pandas as pd
import os
import glob
import tqdm
import matplotlib.pyplot as plt

INPUT_PATH = os.path.join("RxData_Processed_fix", "*", "*", "*.log")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "RX_LEVEL_18"]
df_list = []

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=cols)
    df[cols[0]] = pd.to_datetime(df[cols[0]])
    df[cols[1]] = pd.to_numeric(df[cols[1]])
    df_list.append(df)

df1 = pd.concat(df_list)
df1 = df1.set_index("time")

INPUT_PATH = os.path.join("RxData_Processed", "*", "*", "192.168.100.11_csv.log")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "1803_RX_LEVEL"]
df_list = []

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=cols)
    df[cols[0]] = pd.to_datetime(df[cols[0]])
    df[cols[1]] = pd.to_numeric(df[cols[1]])
    df_list.append(df)

df2 = pd.concat(df_list)
df2 = df2.set_index("time")

INPUT_PATH = os.path.join("RainData_Processed_fix", "*", "*.csv")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "rain"]
df_list = []

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=1, names=cols)
    df[cols[0]] = pd.to_datetime(df[cols[0]])
    df[cols[1]] = pd.to_numeric(df[cols[1]])
    df_list.append(df)

df3 = pd.concat(df_list)
df3 = df3.set_index("time")

df = df1.join(df2).join(df3)
df = df.sort_index()
print(df)

fig = plt.figure()
plt.rcParams["font.family"] = "Hiragino Sans"
plt.plot(df.index, df["RX_LEVEL_18"], label="RX_LEVEL_18", color="blue")
plt.plot(df.index, df["1803_RX_LEVEL"], label="1803_RX_LEVEL", color="orange")
plt.plot(df.index, df["rain"], label="rain", color="green")
plt.xlabel("Time")
plt.ylabel("Values")
plt.title("RxLevelsと降雨量の時系列データ")
plt.legend()
plt.grid()
plt.savefig("RxLevels_RainData.png", dpi=300)
plt.show()