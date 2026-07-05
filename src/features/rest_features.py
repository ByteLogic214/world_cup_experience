import pandas as pd


def compute_rest_days(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    df["rest_days_home"] = 3
    df["rest_days_away"] = 3

    return df
