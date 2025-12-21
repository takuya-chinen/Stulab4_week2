import pandas as pd
import os
import glob
import numpy as np
import datetime
import tqdm

INPUT_PATH = os.path.join("RxData", "*", "*", "*_csv.log")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "1803_RX_LEVEL"]

def check_type(x):
    try:
        x = float(x)
    except (ValueError, TypeError):
        try:
            x = datetime.datetime.strptime(x, '%H:%M:%S')
        except (ValueError, TypeError):
            x = x
    return type(x)

for path in tqdm.tqdm(data_path_list):
    date = path.split("/")[2]
    date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    try:
        df = pd.read_csv(path, header=None, skiprows=2, usecols=[0,1], names=cols)
    except UnicodeDecodeError:
        encodings = ['utf-8', 'cp932', 'latin-1']
        for enc in encodings:
            try:
                df = pd.read_csv(path, header=None, skiprows=2, usecols=[0,1], names=cols, encoding=enc)
                break
            except UnicodeDecodeError:
                continue

    df = df.mask(df.map(check_type) == str, np.nan)
    df = df.dropna()
    
    df["time"] = date + " " + df["time"].astype(str)
    df["time"] = pd.to_datetime(df["time"], format='%Y-%m-%d %H:%M:%S')
    df["1803_RX_LEVEL"] = pd.to_numeric(df["1803_RX_LEVEL"])
    df = df.set_index("time")

    date_range = pd.date_range(start=f"{date} 00:00:00", end=f"{date} 23:59:59", freq="s")
    df_new = pd.DataFrame(index=date_range, columns=df.columns)
    df_new = df_new.infer_objects(copy=False)

    df_new.loc[df.index, :] = df
    df_new = df_new.ffill()
    df_new = df_new.bfill()

    date_range = pd.date_range(start=f"{date} 00:00:00", end=f"{date} 23:59:59", freq="10s")
    df_new = df_new.loc[date_range, :]

    path = path.split("/")
    output_path = os.path.join("RxData_Processed", path[1], path[2])
    os.makedirs(output_path, exist_ok=True)
    df_new.to_csv(output_path + f"/{path[3]}", index_label="datetime")
