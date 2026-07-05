import json
import os
from datetime import datetime
from src.utils.paths import get_path, ensure_dir
from src.utils.logger import get_logger

logger = get_logger()


class BronzeWriter:

    def __init__(self):
        self.path = get_path("bronze")
        ensure_dir(self.path)

    def write(self, source: str, data: dict):

        timestamp = datetime.utcnow().isoformat()

        file_path = os.path.join(
            self.path,
            f"{source}_{int(datetime.utcnow().timestamp())}.json"
        )

        payload = {
            "timestamp": timestamp,
            "source": source,
            "data": data
        }

        with open(file_path, "w") as f:
            json.dump(payload, f)

        logger.info(f"Bronze written: {file_path}")
        return file_path
