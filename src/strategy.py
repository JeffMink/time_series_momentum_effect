import sqlite3
import pandas as pd
import numpy as np

class MomentumSignalGenerator:
    def __init__ (self, db_path="market_data.db", lookback_days=63):
        self.db_path=db_path
        self.lookback_days=lookback_days

    def load_data(self, table_name="daily_close_prices"):
        #Pulls the historical prices from the SQLite database.
        print(f"Connecting to {self.db_path}...")
        conn = sqlite3.connect(self.db_path)
        
        #Load data and set the Date column as the index
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn, index_col='Date')
        
        conn.close()
        return df

    def get_signals(self, prices_df):
        print(f"Calculating {self.lookback_days}-day momentum signals...")
        momentum=prices_df.pct_change(periods=self.lookback_days)
        signals_array=np.where(momentum> 0, 1, -1)

        """
        Set NaN to 0 (days that are less than the lookback period). 
        Otherwise they default to -1. This is better than deleting the rows, as it is 
        easier to align with dates later on.
        """
        signals_array[momentum.isna()] = 0 

        signals_df=pd.DataFrame(signals_array,index=prices_df.index, columns=prices_df.columns)
        return signals_df


if __name__ == "__main__":
 
    generator = MomentumSignalGenerator(lookback_days=63)
    
    prices = generator.load_data()
    signals = generator.get_signals(prices)

    print(signals.tail())
