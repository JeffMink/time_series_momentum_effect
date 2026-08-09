import sqlite3
import pandas as pd

class VolatilityWeightGenerator:
    def __init__ (self, db_path="market_data.db", rolling_std_window=20):
        self.db_path=db_path
        self.rolling_std=rolling_std_window

    def load_data(self, table_name="daily_close_prices"):
        #Pulls the historical prices from the SQLite database.
        print(f"Connecting to {self.db_path}...")
        conn = sqlite3.connect(self.db_path)
        
        #Load data and set the Date column as the index
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn, index_col='Date')
        
        conn.close()
        return df
    
    def get_weights(self,prices_df):
        print(f"Generating weights dataframe. Rolling window is {self.rolling_std}.")
        daily_returns=prices_df.pct_change() 
        rolling_volatility=daily_returns.rolling(window=self.rolling_std).std()
        inverse_volatility=1/rolling_volatility
        inverse_volatility_normalized=inverse_volatility.div(inverse_volatility.sum(axis=1), axis=0)

        return inverse_volatility_normalized


if __name__ == "__main__":
 
    weight_generator = VolatilityWeightGenerator(rolling_std_window=20)

    
    prices = weight_generator.load_data()
    weights = weight_generator.get_weights(prices)

    print(weights.tail())
