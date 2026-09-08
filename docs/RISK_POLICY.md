# ATS Risk Policy

## Principle
Risk controls are deterministic, independently testable, and authoritative. Strategy, prediction, and AI components cannot bypass them.

## Modes
- BACKTEST: no external execution
- PAPER: simulated execution only
- SHADOW: real-time decisions recorded without orders
- LIVE: disabled until all validation gates pass

## Required controls
- Maximum risk per trade
- Maximum daily loss
- Maximum total exposure
- Maximum position size
- Maximum leverage
- Maximum open positions
- Maximum correlated exposure
- Maximum drawdown
- Maximum spread
- Maximum slippage
- Data freshness requirement
- Broker connectivity requirement
- Position reconciliation requirement

## Fail-closed behavior
If market data is stale or inconsistent, broker state cannot be reconciled, execution acknowledgements are ambiguous, risk state is unavailable, or a critical service fails, new orders are blocked. Existing positions follow predefined protective handling; emergency flattening is available where supported.

## Live activation
Live mode requires explicit configuration plus successful backtest, out-of-sample, walk-forward, paper, and shadow validation. Live capital is initially capped to a small allocation and cannot be increased automatically merely because of recent profits.

## No prohibited behaviors
ATS will not use martingale sizing, loss-chasing, unrestricted leverage escalation, or automatic withdrawal/transfer capabilities.
