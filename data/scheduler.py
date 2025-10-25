"""
Scheduler for Oasis
Handles periodic data updates and model retraining
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import sys
import os

# Add the models and data directories to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.lstm_predictor import LSTMPredictor
from data.data_handler import DataHandler

class DataScheduler:
    def __init__(self):
        """Initialize the scheduler"""
        self.scheduler = BlockingScheduler()
        self.data_handler = DataHandler()
        self.models = {}  # Store trained models in memory
        
        # Define symbols to track
        self.stock_symbols = ['TSLA', 'AAPL', 'GOOGL', 'MSFT']
        self.crypto_symbols = ['BTC-USD', 'ETH-USD']
        
    def update_data(self):
        """Update market data for all tracked symbols"""
        print("Updating market data...")
        
        # Update stock data
        for symbol in self.stock_symbols:
            try:
                success = self.data_handler.fetch_and_store_data(
                    symbol, period="1mo", data_type="stock"
                )
                if success:
                    print(f"Updated data for {symbol}")
                else:
                    print(f"Failed to update data for {symbol}")
            except Exception as e:
                print(f"Error updating data for {symbol}: {e}")
        
        # Update crypto data
        for symbol in self.crypto_symbols:
            try:
                success = self.data_handler.fetch_and_store_data(
                    symbol, period="1mo", data_type="crypto"
                )
                if success:
                    print(f"Updated data for {symbol}")
                else:
                    print(f"Failed to update data for {symbol}")
            except Exception as e:
                print(f"Error updating data for {symbol}: {e}")
                
        print("Data update completed.")
    
    def retrain_models(self):
        """Retrain models for all tracked symbols"""
        print("Retraining models...")
        
        # Retrain stock models
        for symbol in self.stock_symbols:
            try:
                print(f"Retraining model for {symbol}...")
                predictor = LSTMPredictor(symbol, period='6mo')
                
                if predictor.fetch_data():
                    predictor.train(epochs=20)
                    self.models[f"{symbol}_stock"] = predictor
                    print(f"Retrained model for {symbol}")
                else:
                    print(f"Failed to fetch data for {symbol}")
            except Exception as e:
                print(f"Error retraining model for {symbol}: {e}")
        
        # Retrain crypto models
        for symbol in self.crypto_symbols:
            try:
                print(f"Retraining model for {symbol}...")
                predictor = LSTMPredictor(symbol, period='6mo')
                
                if predictor.fetch_data():
                    predictor.train(epochs=20)
                    self.models[f"{symbol}_crypto"] = predictor
                    print(f"Retrained model for {symbol}")
                else:
                    print(f"Failed to fetch data for {symbol}")
            except Exception as e:
                print(f"Error retraining model for {symbol}: {e}")
                
        print("Model retraining completed.")
    
    def start_scheduler(self):
        """Start the scheduler with predefined jobs"""
        print("Starting Oasis Scheduler...")
        
        # Add job to update data every hour
        self.scheduler.add_job(
            self.update_data,
            CronTrigger(minute=0),  # Run at minute 0 of every hour
            id='update_data',
            name='Update Market Data',
            replace_existing=True
        )
        
        # Add job to retrain models daily at 2 AM
        self.scheduler.add_job(
            self.retrain_models,
            CronTrigger(hour=2, minute=0),  # Run at 2:00 AM daily
            id='retrain_models',
            name='Retrain Models',
            replace_existing=True
        )
        
        # Start the scheduler
        try:
            print("Scheduler started. Press Ctrl+C to exit.")
            self.scheduler.start()
        except KeyboardInterrupt:
            print("Scheduler stopped.")
            self.scheduler.shutdown()

# Example usage
if __name__ == "__main__":
    scheduler = DataScheduler()
    
    # For testing purposes, you can run individual functions
    if len(sys.argv) > 1:
        if sys.argv[1] == "update":
            scheduler.update_data()
        elif sys.argv[1] == "retrain":
            scheduler.retrain_models()
        else:
            print("Usage: python scheduler.py [update|retrain]")
    else:
        # Start the scheduler
        scheduler.start_scheduler()