import pandas as pd
import os
import glob
import tqdm

INPUT_PATH = os.path.join("RainData_Processed", "*", "*.csv")
data_path_list = glob.glob(INPUT_PATH)
cols = ["time", "rain"]

for path in tqdm.tqdm(data_path_list):
    df = pd.read_csv(path, header=None, skiprows=2, names=cols)

    df["time"] = pd.to_datetime(df["time"])
    df["rain"] = pd.to_numeric(df["rain"])

    df["rain"] = df["rain"].apply(lambda x: x * 0.0083333 * 60)

    df = df.set_index("time")
    path = path.split("/")
    output_path = os.path.join("RainData_Processed_fix", path[1])
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(output_path + f"/{path[2]}", index_label="datetime")