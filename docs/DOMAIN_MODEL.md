# ATS Domain Model

The core domain is broker-neutral. External APIs are translated into these contracts.

## Instrument
Fields: symbol, asset_class, exchange, currency, multiplier, tick_size, contract_expiry (optional), metadata.

Asset classes: EQUITY, OPTION, FUTURE, CRYPTO.

## MarketObservation
Fields: instrument, timestamp, bid, ask, last, volume, bar data, source, freshness.

## FeatureSnapshot
Fields: instrument, timestamp, feature_set_version, values, source_observation_timestamp.

## Signal
Fields: strategy_id, instrument, timestamp, direction, confidence, expected_return, expected_loss, horizon, rationale, feature_set_version.

## TradeIntent
Fields: intent_id, signal_id, instrument, direction, target_quantity, order_type, limit_price (optional), stop_price (optional), take_profit (optional), time_in_force, requested_risk, created_at.

A TradeIntent is not an executable order until approved by Risk Governor.

## RiskDecision
Fields: intent_id, status, approved_quantity, permitted_risk, reasons, risk_policy_version, evaluated_at.

Statuses: APPROVED, REJECTED, HALTED.

## Order
Fields: order_id, broker_order_id (optional), intent_id, instrument, side, quantity, order_type, prices, time_in_force, status, timestamps.

## Fill
Fields: fill_id, order_id, broker_fill_id (optional), quantity, price, fees, timestamp.

## Position
Fields: instrument, quantity, average_price, market_price, realized_pnl, unrealized_pnl, exposure, updated_at.

## PortfolioSnapshot
Fields: account_id, timestamp, cash, equity, buying_power, gross_exposure, net_exposure, daily_pnl, drawdown, positions.

## AuditEvent
Immutable event record for decisions, risk decisions, order lifecycle, fills, errors, state transitions, configuration changes, and emergency actions.
