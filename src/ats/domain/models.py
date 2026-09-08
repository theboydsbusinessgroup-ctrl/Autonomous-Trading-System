from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any

from .enums import (
    AssetClass,
    OrderStatus,
    OrderType,
    RiskDecisionStatus,
    Side,
    TimeInForce,
    TradingMode,
)


@dataclass(frozen=True)
class Instrument:
    symbol: str
    asset_class: AssetClass
    exchange: str | None = None
    currency: str = "USD"


@dataclass(frozen=True)
class MarketObservation:
    instrument: Instrument
    timestamp: datetime
    bid: Decimal | None = None
    ask: Decimal | None = None
    last: Decimal | None = None
    volume: int | None = None

    @property
    def mid(self) -> Decimal | None:
        if self.bid is None or self.ask is None:
            return None
        return (self.bid + self.ask) / Decimal("2")

    def age_seconds(self, now: datetime) -> float:
        return max(0.0, (now - self.timestamp).total_seconds())


@dataclass(frozen=True)
class FeatureSnapshot:
    instrument: Instrument
    timestamp: datetime
    values: dict[str, float]


@dataclass(frozen=True)
class Signal:
    instrument: Instrument
    timestamp: datetime
    strategy: str
    direction: Side
    strength: float
    rationale: str = ""


@dataclass(frozen=True)
class TradeIntent:
    instrument: Instrument
    side: Side
    quantity: Decimal
    strategy: str
    signal_strength: float
    timestamp: datetime
    limit_price: Decimal | None = None
    stop_price: Decimal | None = None


@dataclass(frozen=True)
class RiskDecision:
    status: RiskDecisionStatus
    reason: str
    approved_quantity: Decimal = Decimal("0")
    checks: dict[str, bool] = field(default_factory=dict)


@dataclass
class Order:
    order_id: str
    intent: TradeIntent
    order_type: OrderType
    time_in_force: TimeInForce
    status: OrderStatus = OrderStatus.NEW
    created_at: datetime | None = None


@dataclass(frozen=True)
class Fill:
    order_id: str
    timestamp: datetime
    quantity: Decimal
    price: Decimal
    fee: Decimal = Decimal("0")


@dataclass
class Position:
    instrument: Instrument
    quantity: Decimal = Decimal("0")
    average_price: Decimal = Decimal("0")
    realized_pnl: Decimal = Decimal("0")


@dataclass(frozen=True)
class PortfolioSnapshot:
    timestamp: datetime
    equity: Decimal
    cash: Decimal
    gross_exposure: Decimal
    daily_pnl: Decimal
    drawdown_pct: Decimal
    open_positions: int


@dataclass(frozen=True)
class AuditEvent:
    timestamp: datetime
    event_type: str
    mode: TradingMode
    message: str
    data: dict[str, Any] = field(default_factory=dict)
