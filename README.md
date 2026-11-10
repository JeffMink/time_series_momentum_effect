# Time-series momentum on US sector ETFs

Long/short time-series momentum on the 11 SPDR sector ETFs (XLK, XLF, XLV, XLE, XLI, XLU, XLC, XLY, XLP, XLB, XLRE),
sized by inverse volatility.

- **Signal:** sign of the 63-day return (+1 long, -1 short, 0 flat / not enough history)
- **Sizing:** inverse 20-day volatility, normalised to sum to 1
- **Execution:** positions set at the close of day t are held over day t+1

## Setup

```
pip install -r requirements.txt
python src/data_loader.py   # downloads prices from 2016 and builds market_data.db
python src/backtest.py      # runs the backtest and prints return, drawdown and Sharpe
```

## Layout

- `src/data_loader.py` – downloads close prices with yfinance and saves them to SQLite
- `src/strategy.py` – momentum signals
- `src/inverse_volatility_sizer.py` – position weights
- `src/backtest.py` – strategy returns (optional transaction costs) and the main script
- `src/metrics.py` – equity curve, max drawdown, Sharpe ratio
- `notebooks/01_exploration.ipynb` – exploration using the `src/` modules
