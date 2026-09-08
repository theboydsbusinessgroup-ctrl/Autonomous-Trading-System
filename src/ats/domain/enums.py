from enum import Enum


class AssetClass(str, Enum):
    EQUITY = "equity"
    OPTION = "option"
    FUTURE = "future"
    CRYPTO = "crypto"


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class TimeInForce(str, Enum):
    DAY = "day"
    GTC = "gtc"
    IOC = "ioc"
    FOK = "fok"


class OrderStatus(str, Enum):
    NEW = "new"
    ACCEPTED = "accepted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class RiskDecisionStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    REDUCED = "reduced"


class TradingMode(str, Enum):
    BACKTEST = "backtest"
    PAPER = "paper"
    SHADOW = "shadow"
    LIVE = "live"


class SystemState(str, Enum):
    OFFLINE = "offline"
    PRE_MARKET = "pre_market"
    DATA_VALIDATION = "data_validation"
    MARKET_OPEN = "market_open"
    SCANNING = "scanning"
    ANALYZING = "analyzing"
    TRADING = "trading"
    POSITION_MANAGEMENT = "position_management"
    PRE_CLOSE = "pre_close"
    CLOSING = "closing"
    POST_MARKET = "post_market"
    DEGRADED = "degraded"
    HALTED = "halted"
    EMERGENCY_FLATTEN = "emergency_flatten"
