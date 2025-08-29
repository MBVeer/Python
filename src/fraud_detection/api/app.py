from __future__ import annotations
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
import numpy as np
from pathlib import Path

from fraud_detection.core.schemas import Transaction, Prediction
from fraud_detection.core.detector import AnomalyDetector, MODEL_PATH
from fraud_detection.core.rules import apply_rules
from fraud_detection.features.features import extract_features
from fraud_detection.persistence.db import init_db, SessionLocal, TransactionLog, Alert


app = FastAPI(title="Fraud Detection API")


_detector: AnomalyDetector | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    init_db()
    global _detector
    if Path(MODEL_PATH).exists():
        _detector = AnomalyDetector.load(MODEL_PATH)


@app.post("/predict", response_model=Prediction)
async def predict(tx: Transaction, db=Depends(get_db)):
    global _detector
    tx_dict = tx.model_dump()

    # Rules first
    rule_flag, rule_reason = apply_rules(tx_dict)

    score = 0.0
    is_anomaly = False
    reason = rule_reason

    if _detector is not None:
        X = np.array([extract_features(tx_dict)])
        is_pred, scores = _detector.predict(X)
        score = float(scores[0])
        is_anomaly = bool(is_pred[0]) or rule_flag
    else:
        is_anomaly = rule_flag

    pred = Prediction(
        transaction_id=tx.transaction_id,
        user_id=tx.user_id,
        score=score,
        is_anomaly=is_anomaly,
        reason=reason,
        created_at=datetime.utcnow(),
    )

    # Persist
    log = TransactionLog(
        transaction_id=pred.transaction_id,
        user_id=pred.user_id,
        merchant_id=tx.merchant_id,
        amount=tx.amount,
        currency=tx.currency,
        timestamp=tx.timestamp,
        is_anomaly=pred.is_anomaly,
        score=pred.score,
        reason=pred.reason,
    )
    db.add(log)
    if pred.is_anomaly:
        alert = Alert(
            transaction_id=pred.transaction_id,
            user_id=pred.user_id,
            score=pred.score,
            reason=pred.reason or "Model/rule flagged",
        )
        db.add(alert)
    db.commit()

    return JSONResponse(content=pred.model_dump())

