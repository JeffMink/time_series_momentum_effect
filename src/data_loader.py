import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

class MarketDataLoader:

    def __init__(self,db_name="market_data.db"):
        self.db_name=db_name
        self.tickers = [
            'XLK', 'XLF', 'XLV', 'XLE', 'XLI', 
            'XLU', 'XLC', 'XLY', 'XLP', 'XLB', 'XLRE'
        ]
        self.conn = sqlite3.connect(self.db_name)

    def fetch_prices(self, start_date, end_date):
        print(f'Downloading data from {start_date} to {end_date}')
        raw_data = yf.download(self.tickers, start=start_date, end=end_date)
        close_prices = raw_data['Close']
        return close_prices

    def write_to_db(self, df, table_name='daily_close_prices'):
        print(f"Saving data to table '{table_name}' in {self.db_name}...")
        df.to_sql(table_name, self.conn, if_exists='replace', index=True)
        print("Data successfully saved!")

    def close_connection(self):
        #Closes the database connection to free up memory.
        self.conn.close()



if __name__ == "__main__":

    loader = MarketDataLoader()
    
    df_prices = loader.fetch_prices(start_date="2016-01-01", end_date="2026-08-05")
    
    loader.write_to_db(df_prices)

    loader.close_connection()
