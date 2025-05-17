# Trading Signal Pipeline

Located in `trading_core/`, this system targets penny stocks under $10.

### Logic Chain

1. `get_live_penny_stocks()` returns mocked market data
2. `apply_signal_rules()` checks:
   - Price > EMA
   - Price > VWAP
   - Volume thresholds
3. Output passed to `signal_generator.py`
4. Signals embedded and stored in memory
5. Results visible in frontend via `/api/trading/signals`

### Use Case

- Premarket scanner
- Intraday signal generator
- Signal-to-memory feedback loop
- Agent retrains on signals using log capture
