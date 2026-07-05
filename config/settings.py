# config/settings.py
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import yaml
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class APISettings:
    """Configuración inmutable para la API de fútbol."""
    key: str
    host: str
    base_url: str = field(init=False)
    timeout: int = 30
    max_retries: int = 3
    
    def __post_init__(self):
        object.__setattr__(self, 'base_url', f"https://{self.host}")

@dataclass(frozen=True)
class StorageSettings:
    """Configuración de almacenamiento con rutas validadas."""
    bronze_dir: Path
    silver_dir: Path
    gold_dir: Path
    models_dir: Path
    
    def __post_init__(self):
        # Crear directorios si no existen
        for dir_path in [self.bronze_dir, self.silver_dir, self.gold_dir, self.models_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

@dataclass(frozen=True)
class AppConfig:
    """Configuración principal de la aplicación."""
    env: str
    log_level: str
    api: APISettings
    storage: StorageSettings
    
    @classmethod
    def from_environment(cls) -> 'AppConfig':
        """Factory method que carga configuración desde variables de entorno."""
        api_key = os.getenv("API_FOOTBALL_KEY")
        api_host = os.getenv("API_FOOTBALL_HOST")
        
        if not api_key or not api_host:
            raise ValueError(
                "Variables de entorno API_FOOTBALL_KEY y API_FOOTBALL_HOST son requeridas"
            )
        
        return cls(
            env=os.getenv("PROJECT_ENV", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            api=APISettings(key=api_key, host=api_host),
            storage=StorageSettings(
                bronze_dir=Path(os.getenv("BRONZE_DIR", "data/bronze")),
                silver_dir=Path(os.getenv("SILVER_DIR", "data/silver")),
                gold_dir=Path(os.getenv("GOLD_DIR", "data/gold")),
                models_dir=Path(os.getenv("MODELS_DIR", "models"))
            )
        )
    
    @classmethod
    def from_yaml(cls, config_path: str = "config/config.yaml") -> 'AppConfig':
        """Carga configuración desde archivo YAML con fallback a variables de entorno."""
        try:
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
            
            # Priorizar variables de entorno sobre YAML
            return cls.from_environment()
            
        except FileNotFoundError:
            # Si no hay archivo YAML, usar solo variables de entorno
            return cls.from_environment()

# Singleton global de configuración
_config: Optional[AppConfig] = None

def get_config() -> AppConfig:
    """Obtiene la configuración singleton (lazy initialization)."""
    global _config
    if _config is None:
        _config = AppConfig.from_environment()
    return _config
