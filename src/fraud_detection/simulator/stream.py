from __future__ import annotations
import random
import string
from datetime import datetime, timedelta
from typing import Iterator, Dict


CURRENCIES = ["USD", "EUR", "INR", "GBP"]
CHANNELS = ["web", "mobile", "pos"]


def _rid(prefix: str) -> str:
    return prefix + "_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def generate_transactions(n: int = 1000) -> Iterator[Dict]:
    base_time = datetime.utcnow()
    for i in range(n):
        amt = max(0.5, random.lognormvariate(2.5, 0.8))
        if random.random() < 0.01:
            amt *= 50  # spikes
        yield {
            "transaction_id": _rid("tx"),
            "user_id": _rid("user"),
            "merchant_id": _rid("m"),
            "amount": round(amt, 2),
            "currency": random.choice(CURRENCIES),
            "timestamp": (base_time + timedelta(seconds=i)).isoformat(),
            "ip_address": None,
            "device_id": None,
            "location_lat": None,
            "location_lon": None,
            "card_present": random.random() > 0.3,
            "channel": random.choice(CHANNELS),
        }

