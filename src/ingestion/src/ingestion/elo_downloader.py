import requests
import pandas as pd
from src.utils.logger import get_logger

logger = get_logger()


ELO_URL = "https://eloratings.net/data.json"


def fetch_elo_data():
    logger.info("Downloading Elo ratings...")

    response = requests.get(ELO_URL)

    if response.status_code != 200:
        raise Exception("Failed to download Elo data")

    data = response.json()

    df = pd.DataFrame(data)

    logger.info(f"Elo dataset loaded: {len(df)} records")

    return df
