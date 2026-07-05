import os
from config.settings import config

def get_path(key: str) -> str:
    return config["paths"][key]

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
