import pandas as pd
import os
import glob
import tqdm

INPUT_PATH = os.path.join("RxData_Processed", "*", "*", "192.168.100.9_csv.log")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "1803_RX_LEVEL"]

def fix_data(x):
    if x < 0:
        x += 256
        x = (x / 2) - 256
    else:
        x = (x / 2) - 256
    return x

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=cols)

    df["time"] = pd.to_datetime(df["time"])
    df["1803_RX_LEVEL"] = pd.to_numeric(df["1803_RX_LEVEL"])

    df["1803_RX_LEVEL"] = df["1803_RX_LEVEL"].apply(fix_data)

    df = df.set_index("time")

    path = path.split("/")
    output_path = os.path.join("RxData_Processed_fix", path[1], path[2])
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(output_path + f"/{path[3]}", index_label="datetime")
