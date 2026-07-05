import pandas as pd


def compute_elo_difference(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["elo_difference"] = df["elo_home"] - df["elo_away"]

    return df
