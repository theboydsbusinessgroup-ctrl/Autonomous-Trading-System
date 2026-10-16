# Autonomous Trading System (ATS)

A broker-agnostic, risk-first autonomous trading platform for research, backtesting, paper trading, shadow trading, and—only after validation—small live allocations.

## Supported asset classes
- U.S. equities
- Options
- Futures
- Crypto

## Operating principle
ATS separates prediction, decision, risk, execution, and portfolio management. Deterministic risk controls have authority over strategy and AI components. No live trading is enabled by default.

## Validation path
1. Data integrity
2. Backtesting
3. Out-of-sample validation
4. Walk-forward validation
5. Paper trading
6. Shadow trading
7. Micro-live allocation
8. Controlled scaling

## Initial vertical slice
The first operational implementation is an equity-only paper trader. Interfaces are designed to support additional asset classes and brokers without rewriting the core.

## Safety
- No broker credentials in source control
- Paper/live environments separated
- Fail-closed execution
- Daily loss and exposure limits
- Independent kill switch
- Full audit trail

## Status
Architecture initialized. No live-order functionality is enabled.

Implemented code is a domain-model foundation and optional telemetry adapter. The risk governor, data pipeline, backtester, broker, and paper trader described above are planned; the policy limits in `.env.example` are not enforced by a running system yet.

## Local validation

Python 3.12+ is required. The domain regression tests use only the standard library:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Market observations reject crossed quotes, invalid Decimal prices, and naive timestamps. Their age check rejects future observations instead of treating them as fresh. Trade intents, fills, and risk decisions validate basic quantity and price invariants. These checks support the future risk governor; they do not implement portfolio limits or authorize execution.
