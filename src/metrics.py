import numpy as np

TRADING_DAYS = 252


class PerformanceEvaluator:
    def equity_curve(self, returns):  # cumulative growth of 1 unit
        return (returns + 1).cumprod()

    def drawdown(self, returns):
        equity_curve = self.equity_curve(returns)
        running_max = equity_curve.cummax()
        drawdowns = (equity_curve - running_max) / running_max
        return drawdowns.min()

    def sharpe_ratio(self, returns, risk_free_rate=0.0):
        # risk_free_rate is annual (e.g. 0.04 for 4%); converted to a daily rate.
        excess = returns - risk_free_rate / TRADING_DAYS
        return np.sqrt(TRADING_DAYS) * excess.mean() / excess.std(ddof=1)
