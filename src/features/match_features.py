import pandas as pd


def compute_match_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["goal_diff"] = df["home_goals"] - df["away_goals"]

    df["is_home_advantage"] = 1

    df["total_goals"] = df["home_goals"] + df["away_goals"]

    return df
