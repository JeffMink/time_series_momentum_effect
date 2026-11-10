import sqlite3

import pandas as pd
import yfinance as yf

from paths import DB_PATH


class MarketDataLoader:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.tickers = [
            'XLK', 'XLF', 'XLV', 'XLE', 'XLI',
            'XLU', 'XLC', 'XLY', 'XLP', 'XLB', 'XLRE'
        ]

    def fetch_prices(self, start_date, end_date):
        print(f'Downloading data from {start_date} to {end_date}')
        raw_data = yf.download(self.tickers, start=start_date, end=end_date, auto_adjust=True)
        return raw_data['Close']

    def write_to_db(self, df, table_name='daily_close_prices'):
        print(f"Saving data to table '{table_name}' in {self.db_path}...")
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=True)
        print("Data successfully saved!")


if __name__ == '__main__':
    # Rebuilds market_data.db (it is git-ignored, so this is how to recreate it).
    loader = MarketDataLoader()
    prices = loader.fetch_prices(start_date='2016-01-01', end_date=pd.Timestamp.today().strftime('%Y-%m-%d'))
    loader.write_to_db(prices)
