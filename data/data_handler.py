"""
Data handler for Oasis
Handles data fetching, storage, and management
"""
import yfinance as yf
import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from contextlib import contextmanager

# Load environment variables
load_dotenv()

class DataHandler:
    def __init__(self, db_path=None):
        """
        Initialize the DataHandler
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path or os.getenv('DB_PATH', 'data/market_data.db')
        self.init_database()
        
    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize the SQLite database with required tables and indexes"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create table for stock data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    date DATE NOT NULL,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, date)
                )
            ''')
            
            # Create index on stock_data for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_stock_symbol_date 
                ON stock_data (symbol, date)
            ''')
            
            # Create table for crypto data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crypto_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    date DATE NOT NULL,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, date)
                )
            ''')
            
            # Create index on crypto_data for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_crypto_symbol_date 
                ON crypto_data (symbol, date)
            ''')
            
            conn.commit()
    
    def fetch_and_store_data(self, symbol, period="1y", data_type="stock"):
        """
        Fetch data using yfinance and store it in the database
        
        Args:
            symbol (str): Stock or crypto symbol
            period (str): Period for historical data
            data_type (str): Type of data ('stock' or 'crypto')
        """
        try:
            # Fetch data using yfinance
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                print(f"No data found for {symbol}")
                return False
            
            # Store data in database
            self.store_data(symbol, data, data_type)
            print(f"Successfully fetched and stored {len(data)} records for {symbol}")
            return True
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return False
    
    def store_data(self, symbol, data, data_type="stock"):
        """
        Store data in the database
        
        Args:
            symbol (str): Stock or crypto symbol
            data (DataFrame): Data to store
            data_type (str): Type of data ('stock' or 'crypto')
        """
        with self.get_db_connection() as conn:
            # Prepare data for insertion
            data_to_insert = []
            for index, row in data.iterrows():
                data_to_insert.append((
                    symbol,
                    index.strftime('%Y-%m-%d'),
                    float(row['Open']),
                    float(row['High']),
                    float(row['Low']),
                    float(row['Close']),
                    int(row['Volume'])
                ))
            
            # Insert data
            table_name = "stock_data" if data_type == "stock" else "crypto_data"
            conn.executemany(f'''
                INSERT OR REPLACE INTO {table_name} 
                (symbol, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', data_to_insert)
            
            conn.commit()
            
            print(f"Stored {len(data_to_insert)} records for {symbol}")
    
    def get_historical_data(self, symbol, start_date=None, end_date=None, data_type="stock"):
        """
        Retrieve historical data from the database
        
        Args:
            symbol (str): Stock or crypto symbol
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            data_type (str): Type of data ('stock' or 'crypto')
            
        Returns:
            DataFrame: Historical data
        """
        with self.get_db_connection() as conn:
            # Build query
            table_name = "stock_data" if data_type == "stock" else "crypto_data"
            query = f"SELECT symbol, date, open, high, low, close, volume FROM {table_name} WHERE symbol = ?"
            params = [symbol]
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
                
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
                
            query += " ORDER BY date"
            
            # Execute query
            data = pd.read_sql_query(query, conn, params=params)
            
            return data
    
    def get_latest_data(self, symbol, days=30, data_type="stock"):
        """
        Get the latest data for a symbol
        
        Args:
            symbol (str): Stock or crypto symbol
            days (int): Number of days to retrieve
            data_type (str): Type of data ('stock' or 'crypto')
            
        Returns:
            DataFrame: Latest data
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        return self.get_historical_data(symbol, start_date, end_date, data_type)

# Example usage
if __name__ == "__main__":
    # Create data handler
    handler = DataHandler()
    
    # Fetch and store data for Tesla
    handler.fetch_and_store_data("TSLA", period="1y", data_type="stock")
    
    # Fetch and store data for Bitcoin
    handler.fetch_and_store_data("BTC-USD", period="1y", data_type="crypto")
    
    # Retrieve latest data
    tesla_data = handler.get_latest_data("TSLA", days=7, data_type="stock")
    print("Latest Tesla data:")
    print(tesla_data)