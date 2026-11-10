class VolatilityWeightGenerator:
    def __init__(self, rolling_std_window=20):
        self.rolling_std = rolling_std_window

    def get_weights(self, prices_df):
        print(f"Generating weights dataframe. Rolling window is {self.rolling_std}.")
        daily_returns = prices_df.pct_change(fill_method=None)
        rolling_volatility = daily_returns.rolling(window=self.rolling_std).std()
        inverse_volatility = 1 / rolling_volatility
        return inverse_volatility.div(inverse_volatility.sum(axis=1), axis=0)
