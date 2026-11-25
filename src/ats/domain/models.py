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


def _aware_timestamp(value: datetime, name: str) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")


def _decimal(value: Decimal, name: str, *, positive: bool = False, nonnegative: bool = False) -> None:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError(f"{name} must be a finite Decimal")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    if nonnegative and value < 0:
        raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True)
class Instrument:
    symbol: str
    asset_class: AssetClass
    exchange: str | None = None
    currency: str = "USD"


def _price(value: Decimal, name: str, instrument: Instrument) -> None:
    # Futures can trade below zero; option bid quotes can legitimately be zero.
    if instrument.asset_class == AssetClass.FUTURE:
        _decimal(value, name)
    elif instrument.asset_class == AssetClass.OPTION and name == "bid":
        _decimal(value, name, nonnegative=True)
    else:
        _decimal(value, name, positive=True)


@dataclass(frozen=True)
class MarketObservation:
    instrument: Instrument
    timestamp: datetime
    bid: Decimal | None = None
    ask: Decimal | None = None
    last: Decimal | None = None
    volume: int | None = None

    def __post_init__(self) -> None:
        _aware_timestamp(self.timestamp, "timestamp")
        for name in ("bid", "ask", "last"):
            value = getattr(self, name)
            if value is not None:
                _price(value, name, self.instrument)
        if self.bid is not None and self.ask is not None and self.bid > self.ask:
            raise ValueError("bid must not exceed ask")
        if self.volume is not None and (type(self.volume) is not int or self.volume < 0):
            raise ValueError("volume must be a nonnegative integer")

    @property
    def mid(self) -> Decimal | None:
        if self.bid is None or self.ask is None:
            return None
        return (self.bid + self.ask) / Decimal("2")

    def age_seconds(self, now: datetime) -> float:
        _aware_timestamp(now, "now")
        age = (now - self.timestamp).total_seconds()
        if age < 0:
            raise ValueError("market observation is dated in the future")
        return age


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

    def __post_init__(self) -> None:
        _aware_timestamp(self.timestamp, "timestamp")
        _decimal(self.quantity, "quantity", positive=True)
        for name in ("limit_price", "stop_price"):
            value = getattr(self, name)
            if value is not None:
                _price(value, name, self.instrument)


@dataclass(frozen=True)
class RiskDecision:
    status: RiskDecisionStatus
    reason: str
    approved_quantity: Decimal = Decimal("0")
    checks: dict[str, bool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.status, RiskDecisionStatus):
            raise ValueError("status must be a RiskDecisionStatus")
        _decimal(self.approved_quantity, "approved_quantity", nonnegative=True)
        if self.status == RiskDecisionStatus.REJECTED and self.approved_quantity != 0:
            raise ValueError("rejected decisions cannot approve a quantity")
        if self.status != RiskDecisionStatus.REJECTED and self.approved_quantity <= 0:
            raise ValueError("approved or reduced decisions require a positive quantity")


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

    def __post_init__(self) -> None:
        _aware_timestamp(self.timestamp, "timestamp")
        _decimal(self.quantity, "quantity", positive=True)
        # Fill has no instrument; signed futures prices must remain representable.
        _decimal(self.price, "price")
        _decimal(self.fee, "fee")  # Signed fees permit exchange rebates.


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
