import pandas as pd
import os
import glob
import tqdm
import matplotlib.pyplot as plt

INPUT_PATH = os.path.join("RxData_Processed_fix", "*", "*", "*.log")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "RX_LEVEL_18"]
freq = -3

df_list = []

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=cols)
    df[cols[0]] = pd.to_datetime(df[cols[0]])
    df[cols[1]] = pd.to_numeric(df[cols[1]])
    df_list.append(df)

df1 = pd.concat(df_list)
print(f"最大値: {df1['RX_LEVEL_18'].max()}")
print(f"最小値: {df1['RX_LEVEL_18'].min()}")

level = []
count = []
sum_sec = []
min_level = int(df1[cols[1]].min()) - 1
for i in range(0, min_level, freq):
    level.append(i)
    count.append(((df1[cols[1]] <= i) & (df1[cols[1]] > i + freq)).sum())
df = pd.DataFrame({"rx_level": level[::-1], "count": count[::-1]})
df["count"] = df["count"].cumsum()
total = df["count"].iloc[-1]
df["ratio"] = df["count"] / total * 100
df["ratio"] = df["ratio"].replace(0, 1e-6)

plt.rcParams["font.family"] = "Hiragino Sans"
fig, ax = plt.subplots()
ax.plot(df["ratio"], df["rx_level"], label="受信強度(dB)", marker=".")
ax.set_xscale("log")
ax.set_xlabel("累積時間率(%)")
ax.set_ylabel("受信強度(dB)")
ax.set_title("受信強度累積時間分布 18GHz(琉大観測: 2009/06, 2009/10 〜 2009/12)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(float(x))))
plt.legend()
plt.savefig("rx_dist_18.png")
# plt.show()