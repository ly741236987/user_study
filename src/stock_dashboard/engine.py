from __future__ import annotations

from dataclasses import dataclass
from math import floor

from .models import StockSnapshot, TradeSuggestion


@dataclass
class EngineConfig:
    buy_threshold: float = 0.35
    sell_threshold: float = -0.35
    max_position_pct: float = 0.12
    lot_size: int = 100


class RecommendationEngine:
    """Simple deterministic strategy for a first version dashboard.

    Notes:
    - `signal_score` range is expected in [-1, 1].
    - Suggestions are for educational/demo use only and are not financial advice.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()

    def suggest(
        self,
        snapshot: StockSnapshot,
        cash: float,
        holding_qty: int,
    ) -> TradeSuggestion:
        if snapshot.signal_score >= self.config.buy_threshold:
            qty = self._buy_quantity(snapshot.price, cash)
            if qty > 0:
                return TradeSuggestion(
                    code=snapshot.code,
                    name=snapshot.name,
                    action="BUY",
                    quantity=qty,
                    reason=(
                        f"signal_score={snapshot.signal_score:.2f} >= buy_threshold={self.config.buy_threshold:.2f}"
                    ),
                    timestamp=snapshot.timestamp,
                )

        if snapshot.signal_score <= self.config.sell_threshold and holding_qty > 0:
            qty = self._sell_quantity(holding_qty)
            if qty > 0:
                return TradeSuggestion(
                    code=snapshot.code,
                    name=snapshot.name,
                    action="SELL",
                    quantity=qty,
                    reason=(
                        f"signal_score={snapshot.signal_score:.2f} <= sell_threshold={self.config.sell_threshold:.2f}"
                    ),
                    timestamp=snapshot.timestamp,
                )

        return TradeSuggestion(
            code=snapshot.code,
            name=snapshot.name,
            action="HOLD",
            quantity=0,
            reason="signal in neutral range or insufficient cash/position",
            timestamp=snapshot.timestamp,
        )

    def _buy_quantity(self, price: float, cash: float) -> int:
        budget = cash * self.config.max_position_pct
        lots = floor(budget / (price * self.config.lot_size))
        return max(lots, 0) * self.config.lot_size

    def _sell_quantity(self, holding_qty: int) -> int:
        half = floor((holding_qty / 2) / self.config.lot_size) * self.config.lot_size
        if half > 0:
            return half
        return holding_qty if holding_qty >= self.config.lot_size else 0
