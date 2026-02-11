from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


Action = Literal["BUY", "SELL", "HOLD"]


@dataclass
class StockSnapshot:
    code: str
    name: str
    price: float
    change_pct: float
    signal_score: float
    timestamp: datetime


@dataclass
class TradeSuggestion:
    code: str
    name: str
    action: Action
    quantity: int
    reason: str
    timestamp: datetime
