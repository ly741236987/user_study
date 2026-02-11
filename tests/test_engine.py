from datetime import datetime

from src.stock_dashboard.engine import EngineConfig, RecommendationEngine
from src.stock_dashboard.models import StockSnapshot


def test_buy_signal_generates_buy_suggestion() -> None:
    engine = RecommendationEngine(EngineConfig(buy_threshold=0.4, max_position_pct=0.2, lot_size=100))
    snapshot = StockSnapshot(
        code="000001",
        name="平安银行",
        price=10.0,
        change_pct=1.2,
        signal_score=0.7,
        timestamp=datetime.now(),
    )

    result = engine.suggest(snapshot=snapshot, cash=100000, holding_qty=0)

    assert result.action == "BUY"
    assert result.quantity == 2000


def test_sell_signal_generates_sell_suggestion() -> None:
    engine = RecommendationEngine(EngineConfig(sell_threshold=-0.3, lot_size=100))
    snapshot = StockSnapshot(
        code="000001",
        name="平安银行",
        price=10.0,
        change_pct=-1.2,
        signal_score=-0.9,
        timestamp=datetime.now(),
    )

    result = engine.suggest(snapshot=snapshot, cash=100000, holding_qty=900)

    assert result.action == "SELL"
    assert result.quantity == 400


def test_neutral_signal_is_hold() -> None:
    engine = RecommendationEngine(EngineConfig(buy_threshold=0.4, sell_threshold=-0.4))
    snapshot = StockSnapshot(
        code="000001",
        name="平安银行",
        price=10.0,
        change_pct=0.1,
        signal_score=0.0,
        timestamp=datetime.now(),
    )

    result = engine.suggest(snapshot=snapshot, cash=100000, holding_qty=1000)

    assert result.action == "HOLD"
    assert result.quantity == 0
