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
        # src/models/poisson.py

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
from scipy.stats import poisson
from statsmodels.api import GLM
from statsmodels.genmod.families import Poisson

from src.models.base import BaseModel


class PoissonModel(BaseModel):
    """
    Modelo Poisson para predicción de goles.

    Se entrena un modelo independiente para:

        - goles_local
        - goles_visitante

    La salida son los lambdas (μ) de ambas distribuciones
    de Poisson.

    A partir de ellos se obtiene:

        P(Local gana)
        P(Empate)
        P(Visitante gana)

    y cualquier marcador exacto.
    """

    def __init__(
        self,
        max_goals: int = 10
    ):

        super().__init__("poisson")

        self.max_goals = max_goals

        self.home_model = None

        self.away_model = None

        self.features: list[str] = []

    def fit(
        self,
        X: pd.DataFrame,
        y_home: pd.Series,
        y_away: pd.Series,
    ) -> None:

        self.features = list(X.columns)

        self.home_model = GLM(
            y_home,
            X,
            family=Poisson()
        ).fit()

        self.away_model = GLM(
            y_away,
            X,
            family=Poisson()
        ).fit()

    def predict(
        self,
        X: pd.DataFrame,
    ) -> pd.DataFrame:

        home_lambda = self.home_model.predict(X)

        away_lambda = self.away_model.predict(X)

        return pd.DataFrame(
            {
                "home_lambda": home_lambda,
                "away_lambda": away_lambda,
            }
        )

    def predict_score_matrix(
        self,
        X: pd.DataFrame,
    ) -> Sequence[np.ndarray]:

        lambdas = self.predict(X)

        matrices = []

        goals = np.arange(
            self.max_goals + 1
        )

        for _, row in lambdas.iterrows():

            home_probs = poisson.pmf(
                goals,
                row.home_lambda
            )

            away_probs = poisson.pmf(
                goals,
                row.away_lambda
            )

            matrix = np.outer(
                home_probs,
                away_probs
            )

            matrices.append(matrix)

        return matrices

    def predict_match_probabilities(
        self,
        X: pd.DataFrame,
    ) -> pd.DataFrame:

        matrices = self.predict_score_matrix(X)

        home = []

        draw = []

        away = []

        for matrix in matrices:

            p_home = 0.0
            p_draw = 0.0
            p_away = 0.0

            rows, cols = matrix.shape

            for i in range(rows):

                for j in range(cols):

                    if i > j:

                        p_home += matrix[i, j]

                    elif i == j:

                        p_draw += matrix[i, j]

                    else:

                        p_away += matrix[i, j]

            total = p_home + p_draw + p_away

            home.append(p_home / total)

            draw.append(p_draw / total)

            away.append(p_away / total)

        return pd.DataFrame(
            {
                "home_win": home,
                "draw": draw,
                "away_win": away,
            }
        )

    def predict_exact_score(
        self,
        X: pd.DataFrame,
    ):

        matrices = self.predict_score_matrix(X)

        predictions = []

        for matrix in matrices:

            idx = np.unravel_index(
                np.argmax(matrix),
                matrix.shape
            )

            predictions.append(
                {
                    "home_goals": int(idx[0]),
                    "away_goals": int(idx[1]),
                    "probability": float(matrix[idx]),
                }
            )

        return pd.DataFrame(predictions)

    def log_likelihood(
        self,
        X: pd.DataFrame,
        y_home: pd.Series,
        y_away: pd.Series,
    ):

        pred = self.predict(X)

        ll_home = poisson.logpmf(
            y_home,
            pred.home_lambda
        ).sum()

        ll_away = poisson.logpmf(
            y_away,
            pred.away_lambda
        ).sum()

        return float(ll_home + ll_away)

    def aic(self):

        return (
            self.home_model.aic
            + self.away_model.aic
        )

    def bic(self):

        return (
            self.home_model.bic
            + self.away_model.bic
        )

    def summary(self):

        return {
            "home": self.home_model.summary(),
            "away": self.away_model.summary(),
}
