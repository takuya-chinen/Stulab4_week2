import pandas as pd
import os
import glob
import tqdm
import matplotlib.pyplot as plt

INPUT_PATH = os.path.join("RainData_Processed_fix", "*", "*.csv")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "rain"]
freq = 3

df_list = []

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=cols)
    df[cols[0]] = pd.to_datetime(df[cols[0]])
    df[cols[1]] = pd.to_numeric(df[cols[1]])
    df_list.append(df)

df1 = pd.concat(df_list)
print(f"最大値: {df1['rain'].max()}")
print(f"最小値: {df1['rain'].min()}")

level = []
count = []
max_rain = int(df1[cols[1]].max()) + 1
for i in range(0, max_rain, freq):
    level.append(i)
    count.append(((df1[cols[1]] >= i) & (df1[cols[1]] < i + freq)).sum())
df = pd.DataFrame({"rx_level": level[::-1], "count": count[::-1]})
df["count"] = df["count"].cumsum()
total = df["count"].iloc[-1]
df["ratio"] = df["count"] / total * 100
df["ratio"] = df["ratio"].replace(0, 1e-6)

plt.rcParams["font.family"] = "Hiragino Sans"
fig, ax = plt.subplots()
ax.plot(df["ratio"], df["rx_level"], label="降雨強度(mm/h)", marker=".")
ax.set_xscale("log")
ax.set_xlabel("累積時間率(%)")
ax.set_ylabel("降雨強度(mm/h)")
ax.set_title("1時間降雨強度累積時間分布")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(float(x))))
plt.legend()
plt.savefig("rain_dist.png")
# plt.show()