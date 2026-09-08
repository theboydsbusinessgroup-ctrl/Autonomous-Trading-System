# ATS System Architecture

## 1. Core flow

Market Data -> Feature Engine -> Strategy Engine -> Decision Engine -> Risk Governor -> Execution Engine -> Broker Adapter -> Portfolio Reconciliation.

Cross-cutting services: orchestration, persistence, observability, notifications, security, model registry, and backtesting.

## 2. Runtime states

OFFLINE -> PRE_MARKET -> DATA_VALIDATION -> MARKET_OPEN -> SCANNING -> ANALYZING -> TRADING -> POSITION_MANAGEMENT -> PRE_CLOSE -> CLOSING -> POST_MARKET -> OFFLINE.

Emergency states: DEGRADED, HALTED, EMERGENCY_FLATTEN.

## 3. Service boundaries

### Market Data
Normalizes historical and streaming market data behind a provider-neutral interface. Validates timestamps, missing data, stale quotes, symbol identity, and session status.

### Feature Engine
Transforms normalized observations into reproducible features. Features must be timestamp-safe and must not use future information.

### Strategy Engine
Independent strategies emit typed trade candidates rather than broker orders. Initial research strategies: momentum, breakout, VWAP, mean reversion, and trend following.

### Decision Engine
Ranks candidates using probability estimates, expected value, costs, liquidity, market regime, strategy health, and portfolio context.

### Risk Governor
A deterministic authority between decisions and execution. It can reject any proposed trade. Enforces per-trade risk, daily loss, exposure, leverage, concentration, correlation, drawdown, spread, slippage, and system-health limits.

### Execution Engine
Converts approved intents into orders and tracks acknowledgements, fills, partial fills, cancellations, rejects, and reconciliation. It contains no strategy logic.

### Broker Adapters
Expose a common interface for account, positions, quotes, orders, cancellations, and reconciliation. Initial broker candidate: Interactive Brokers. Architecture remains broker-agnostic.

### Portfolio Service
Maintains positions, cash, realized/unrealized P&L, exposure, and reconciliation against broker state.

### Orchestrator
Controls startup, market-session lifecycle, service health, graceful shutdown, and emergency transitions.

### Research / Backtesting
Uses point-in-time data and realistic transaction-cost/slippage assumptions. Supports train/validation/test and walk-forward evaluation.

### Observability
Structured logs, metrics, audit events, health checks, alerts, and daily reports.

## 4. AI boundary

AI/LLM components may provide contextual analysis, research, anomaly interpretation, and diagnostics. They cannot override deterministic risk controls. AI output is treated as an input to the decision layer, not as unrestricted execution authority.

## 5. Environment separation

Development, backtest, paper, shadow, and live environments are isolated. Live mode is disabled until validation gates are satisfied.

## 6. Initial deployment target

Equity-only autonomous paper trading. The core contracts remain extensible to options, futures, crypto, and additional brokers.
