import sqlite3

import pandas as pd

from paths import DB_PATH


class ReturnCalculator:
    def __init__(self, db_path=DB_PATH, cost_bps=0.0):
        self.db_path = db_path
        self.cost_bps = cost_bps  # transaction cost per unit of turnover, in basis points

    def load_data(self, table_name="daily_close_prices"):
        # Pulls the historical prices from the SQLite database.
        print(f"Connecting to {self.db_path}...")
        with sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True) as conn:  # read-only: never creates an empty db
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn, index_col='Date')
        df.index = pd.to_datetime(df.index)  # real dates, so date slicing is inclusive and correct
        return df

    def get_returns(self, prices_df, signals_df, weights_df):
        print("Calculating returns")
        returns = prices_df.pct_change(fill_method=None)
        # Positions decided at day t's close are held over day t+1 (prevents lookahead bias)
        positions = (signals_df * weights_df).shift(1).fillna(0)

        gross_return = (returns * positions).sum(axis=1)
        turnover = positions.diff().abs().sum(axis=1)
        costs = turnover * self.cost_bps / 10_000
        return gross_return - costs


if __name__ == '__main__':
    from strategy import MomentumSignalGenerator
    from inverse_volatility_sizer import VolatilityWeightGenerator
    from metrics import PerformanceEvaluator

    lookback_days = 63
    rolling_std_window = 30
    start_date, end_date = '2025-01-01', '2025-12-31'
    cost_bps = 1  # e.g. 5.0 for 5 bps per unit traded

    signals_generator = MomentumSignalGenerator(lookback_days=lookback_days)
    weights_generator = VolatilityWeightGenerator(rolling_std_window=rolling_std_window)
    returns_generator = ReturnCalculator(cost_bps=cost_bps)
    metrics_generator = PerformanceEvaluator()

    # 1. Load the full history (so signals are warmed up before the evaluation window)
    prices = returns_generator.load_data()

    # 2. Generate signals and weights
    signals = signals_generator.get_signals(prices)
    weights = weights_generator.get_weights(prices_df=prices)

    # 3. Calculate daily returns, then restrict to the evaluation window
    returns = returns_generator.get_returns(prices_df=prices, signals_df=signals, weights_df=weights)
    returns = returns.loc[start_date:end_date]

    # 4. Evaluate performance
    equity_curve = metrics_generator.equity_curve(returns)
    cumulative_return = equity_curve.iloc[-1] - 1
    sharpe_ratio = metrics_generator.sharpe_ratio(returns)
    max_drawdown = metrics_generator.drawdown(returns)

    print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()} ({len(returns)} days)")
    print(f"Total Cumulative Return: {cumulative_return * 100:.2f}%")
    print(f"Maximum Drawdown: {max_drawdown * 100:.2f}%")
    print(f"Annualized Sharpe Ratio: {sharpe_ratio:.2f}")
