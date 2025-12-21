import pandas as pd
import os
import glob
import datetime
import tqdm

INPUT_PATH = os.path.join("RainData", "*", "*.csv")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "rain"]

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
    date = path.split("/")[1]
    date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    try:
        df = pd.read_csv(path, header=None, skiprows=2, names=cols)
    except UnicodeDecodeError:
        encodings = ['utf-8', 'cp932', 'latin-1']
        for enc in encodings:
            try:
                df = pd.read_csv(path, header=None, skiprows=2, names=cols, encoding=enc)
                break
            except UnicodeDecodeError:
                continue

    df["time"] = df["time"].apply(lambda x: x.replace("/","-"))
    # df = df["time"].astype(str).str.replace("/", "-", regex=False)
    df["time"] = pd.to_datetime(df["time"], errors='coerce')
    df["rain"] = pd.to_numeric(df["rain"], errors='coerce')

    df = df.dropna(subset=["rain"])
    df = df.dropna(subset=["time"])
    df = df.set_index("time")

    date_range = pd.date_range(start=f"{date} 00:00:00", end=f"{date} 23:59:59", freq="10s")
    df_new = pd.DataFrame(index=date_range, columns=df.columns)
    df_new = df_new.infer_objects(copy=False)

    df_new.loc[df.index, :] = df
    df_new = df_new.ffill().bfill().fillna(0)

    path = path.split("/")
    output_path = os.path.join("RainData_Processed", path[1])
    os.makedirs(output_path, exist_ok=True)
    df_new.to_csv(output_path + f"/{path[2]}", index_label="datetime")