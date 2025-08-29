from __future__ import annotations
import json
from pathlib import Path
import numpy as np

from fraud_detection.core.detector import AnomalyDetector, MODEL_PATH
from fraud_detection.features.features import extract_features


def main():
    raw_path = Path("data/sample_transactions.jsonl")
    if not raw_path.exists():
        print(f"No training data found at {raw_path}. Provide JSONL of transactions.")
        return

    X = []
    with raw_path.open() as f:
        for line in f:
            try:
                obj = json.loads(line)
                X.append(extract_features(obj))
            except Exception:
                continue
    if not X:
        print("No valid training rows.")
        return

    X_arr = np.array(X)
    det = AnomalyDetector()
    det.fit(X_arr)
    det.save(MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()

