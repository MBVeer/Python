from __future__ import annotations
from typing import Dict, Tuple


def apply_rules(tx: Dict) -> Tuple[bool, str | None]:
    """Simple heuristic rules for quick flags.

    Returns: (is_flagged, reason)
    """
    amount = float(tx.get("amount", 0))
    card_present = tx.get("card_present")
    channel = (tx.get("channel") or "").lower()

    if amount >= 5000:
        return True, "High amount >= 5000"
    if (channel == "web" or channel == "mobile") and card_present is False and amount >= 1000:
        return True, "High ecom no-card-present >= 1000"
    return False, None

