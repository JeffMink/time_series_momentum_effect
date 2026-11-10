import numpy as np
import pandas as pd


class MomentumSignalGenerator:
    def __init__(self, lookback_days=63):
        self.lookback_days = lookback_days

    def get_signals(self, prices_df):
        print(f"Calculating {self.lookback_days}-day momentum signals...")
        momentum = prices_df.pct_change(periods=self.lookback_days, fill_method=None)

        # +1 for positive momentum, -1 for negative, 0 for exactly flat.
        # Days inside the lookback window (NaN momentum) are set to 0 rather than dropped,
        # so the frame stays aligned with the price dates.
        signals_array = np.sign(momentum.to_numpy())
        signals_array[np.isnan(signals_array)] = 0

        return pd.DataFrame(signals_array.astype(int), index=prices_df.index, columns=prices_df.columns)
