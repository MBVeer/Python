from __future__ import annotations
from typing import List


NUMERIC_DEFAULT = 0.0


FEATURE_ORDER: List[str] = [
    "amount",
    "card_present",
]


def _bool_to_float(value: bool | None) -> float:
    if value is None:
        return NUMERIC_DEFAULT
    return 1.0 if value else 0.0


def extract_features(transaction: dict) -> List[float]:
    amount = float(transaction.get("amount", NUMERIC_DEFAULT))
    card_present = _bool_to_float(transaction.get("card_present"))
    return [amount, card_present]

