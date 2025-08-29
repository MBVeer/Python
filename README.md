# Real-time Fraud Detection

Python real-time fraud detection system with streaming simulator, anomaly detection, and FastAPI service.

## Quickstart

1) Create a virtual environment and install deps:
``npython -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
``n
2) Start the API:
``nuvicorn fraud_detection.api.app:app --host 0.0.0.0 --port 8000 --reload
``n
3) (Optional) Simulate streaming transactions to the API:
``npython scripts/simulate_send.py
``n
4) (Optional) Train the anomaly detector using a JSONL file at data/sample_transactions.jsonl:
``npython scripts/train.py
``n
## Endpoints
- POST /predict: send a transaction payload and receive anomaly score/flag.

## Notes
- SQLite used for simple persistence at data/fraud.sqlite.
- Model saved in models/isoforest.joblib after training.