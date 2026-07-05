import requests
from config.settings import settings, config
from src.utils.logger import get_logger
from src.utils.paths import get_path, ensure_dir
import json
import time
from datetime import datetime

logger = get_logger()


class APIFootballClient:
    def __init__(self):
        self.base_url = config["api_football"]["base_url"]
        self.headers = {
            "x-apisports-key": settings.API_KEY
        }

    def get_matches(self, league: int, season: int):
        url = f"{self.base_url}/fixtures"
        params = {"league": league, "season": season}

        logger.info(f"Requesting API-Football: {params}")

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")

        return response.json()


def save_bronze(data: dict, name: str):
    path = get_path("bronze")
    ensure_dir(path)

    timestamp = datetime.utcnow().isoformat()
    file_path = f"{path}/{name}_{int(time.time())}.json"

    payload = {
        "timestamp": timestamp,
        "source": "api_football",
        "data": data
    }

    with open(file_path, "w") as f:
        json.dump(payload, f)

    logger.info(f"Saved bronze file: {file_path}")
    return file_path
