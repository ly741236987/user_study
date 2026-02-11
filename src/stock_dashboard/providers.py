from __future__ import annotations

from datetime import datetime

from .models import StockSnapshot


class StockProvider:
    """Abstract provider: replace mock provider with real source integrations.

    Real-world integration candidates:
    - Licensed APIs / data vendors
    - Your own broker API

    For Eastmoney / Tonghuashun, confirm legality, ToS, and API availability first.
    """

    def fetch_all(self) -> list[StockSnapshot]:
        raise NotImplementedError


class MockStockProvider(StockProvider):
    def fetch_all(self) -> list[StockSnapshot]:
        now = datetime.now()
        return [
            StockSnapshot(code="600519", name="贵州茅台", price=1678.20, change_pct=1.34, signal_score=0.62, timestamp=now),
            StockSnapshot(code="000858", name="五粮液", price=129.55, change_pct=-0.41, signal_score=0.12, timestamp=now),
            StockSnapshot(code="300750", name="宁德时代", price=181.30, change_pct=-2.05, signal_score=-0.57, timestamp=now),
            StockSnapshot(code="600036", name="招商银行", price=33.24, change_pct=0.45, signal_score=0.39, timestamp=now),
            StockSnapshot(code="601318", name="中国平安", price=42.01, change_pct=-0.88, signal_score=-0.22, timestamp=now),
        ]
