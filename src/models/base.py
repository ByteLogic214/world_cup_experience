from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


class BaseModel(ABC):
    """
    Clase base para todos los modelos del proyecto.

    Todos los modelos (Poisson, Ridge, XGBoost,
    LightGBM, CatBoost, LSTM, etc.) deberán heredar
    de esta clase para mantener una interfaz única.
    """

    def __init__(self, name: str):

        self.name = name
        self.model = None
        self.features = []

    @abstractmethod
    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series
    ) -> None:
        """
        Entrena el modelo.
        """
        pass

    @abstractmethod
    def predict(
        self,
        X: pd.DataFrame
    ):
        """
        Predicción puntual.
        """
        pass

    def predict_proba(
        self,
        X: pd.DataFrame
    ):
        """
        Algunos modelos no implementan probabilidades.
        """

        raise NotImplementedError(
            f"{self.name} no implementa predict_proba()."
        )

    def save(
        self,
        output_dir: str
    ):

        output = Path(output_dir)

        output.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            self.model,
            output / f"{self.name}.joblib"
        )

    def load(
        self,
        model_path: str
    ):

        self.model = joblib.load(model_path)

    def set_features(
        self,
        features: list[str]
    ):

        self.features = features

    def get_features(self):

        return self.features

    def get_name(self):

        return self.name
