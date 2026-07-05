import pandas as pd
import os

def save_csv(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

def load_csv(path: str):
    return pd.read_csv(path)
