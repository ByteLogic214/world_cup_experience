import os
import yaml
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY = os.getenv("API_FOOTBALL_KEY")
    API_HOST = os.getenv("API_FOOTBALL_HOST")
    ENV = os.getenv("PROJECT_ENV", "dev")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def load_yaml(path="config/config.yaml"):
        with open(path, "r") as f:
            return yaml.safe_load(f)

settings = Settings()
config = Settings.load_yaml()
