import pandas as pd
from src.utils.logger import get_logger

logger = get_logger()


def load_dataset(path: str):
    logger.info(f"Loading local dataset: {path}")

    df = pd.read_csv(path)

    logger.info(f"Loaded dataset: {len(df)} rows")

    return df


def load_all(local_files: list):
    datasets = {}

    for file in local_files:
        datasets[file] = load_dataset(file)

    return datasets
