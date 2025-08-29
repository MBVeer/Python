from __future__ import annotations
from pathlib import Path
from typing import Optional, Tuple
from joblib import dump, load
from sklearn.ensemble import IsolationForest
import numpy as np


MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "isoforest.joblib"


class AnomalyDetector:
    def __init__(self, random_state: int = 42, contamination: float = 0.02):
        self.model = IsolationForest(
            n_estimators=200,
            max_samples="auto",
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1,
        )

    def fit(self, X: np.ndarray) -> None:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        self.model.fit(X)

    def save(self, path: Path = MODEL_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        dump(self.model, path)

    @classmethod
    def load(cls, path: Path = MODEL_PATH) -> "AnomalyDetector":
        det = cls()
        det.model = load(path)
        return det

    def score(self, X: np.ndarray) -> np.ndarray:
        # Higher = more anomalous; invert scikit's anomaly score sign
        return -self.model.score_samples(X)

    def predict(self, X: np.ndarray, threshold: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        scores = self.score(X)
        if threshold is None:
            preds = self.model.predict(X)  # 1 normal, -1 anomaly
            is_anom = (preds == -1)
        else:
            is_anom = scores >= threshold
        return is_anom.astype(bool), scores

