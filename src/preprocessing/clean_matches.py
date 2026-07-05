import pandas as pd
from src.utils.logger import get_logger

logger = get_logger()


def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    logger.info("Cleaning dataset...")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(subset=["date"])

    df = df.sort_values("date")

    df = df.drop_duplicates(subset=["match_id"])

    return df
