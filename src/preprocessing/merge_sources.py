import pandas as pd
from src.utils.logger import get_logger

logger = get_logger()


def merge_datasets(dfs: list) -> pd.DataFrame:
    logger.info(f"Merging {len(dfs)} datasets...")

    merged = pd.concat(dfs, ignore_index=True)

    merged = merged.drop_duplicates(subset=["match_id"])

    logger.info(f"Merged dataset size: {len(merged)}")

    return merged
