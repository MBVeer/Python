from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: str = Field(...)
    user_id: str = Field(...)
    merchant_id: str = Field(...)
    amount: float = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=3)
    timestamp: datetime = Field(...)
    ip_address: Optional[str] = None
    device_id: Optional[str] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    card_present: Optional[bool] = None
    channel: Optional[str] = None  # web, mobile, pos


class Prediction(BaseModel):
    transaction_id: str
    user_id: str
    score: float
    is_anomaly: bool
    reason: Optional[str] = None
    created_at: datetime

