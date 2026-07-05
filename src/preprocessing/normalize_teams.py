import pandas as pd

TEAM_MAP = {
    "USA": "United States",
    "México": "Mexico",
    "Brasil": "Brazil",
    "England": "England",
    "España": "Spain",
    "Deutschland": "Germany",
}


def normalize_team(name: str) -> str:
    if pd.isna(name):
        return name
    return TEAM_MAP.get(name, name)


def apply_team_normalization(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["home_team"] = df["home_team"].apply(normalize_team)
    df["away_team"] = df["away_team"].apply(normalize_team)

    return df
