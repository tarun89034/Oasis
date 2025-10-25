"""
Demo workflow for Oasis
Demonstrates the complete workflow from data fetching to prediction
"""
import sys
import os

# Add the models and data directories to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from models.lstm_predictor import LSTMPredictor
from data.data_handler import DataHandler

def demo_stock_prediction():
    """Demo stock prediction workflow"""
    print("=== Stock Prediction Demo ===")
    
    # 1. Create predictor
    print("1. Creating LSTM predictor for Tesla (TSLA)...")
    predictor = LSTMPredictor('TSLA', period='1y')
    
    # 2. Fetch data
    print("2. Fetching historical data...")
    if predictor.fetch_data():
        print(f"   Successfully fetched {len(predictor.data)} days of data")
    else:
        print("   Failed to fetch data")
        return
    
    # 3. Show recent prices
    print("3. Recent closing prices:")
    print(predictor.data['Close'].tail())
    
    # 4. Train model
    print("4. Training LSTM model...")
    history = predictor.train(epochs=20, batch_size=32)
    print("   Model training completed")
    
    # 5. Make prediction
    print("5. Making prediction...")
    next_day_price = predictor.predict_next_day()
    current_price = predictor.data['Close'][-1]
    
    print(f"   Current price: ${current_price:.2f}")
    print(f"   Predicted next day price: ${next_day_price:.2f}")
    
    # 6. Calculate change
    change = next_day_price - current_price
    change_percent = (change / current_price) * 100
    
    print(f"   Predicted change: ${change:.2f} ({change_percent:.2f}%)")
    
    # 7. Evaluate model
    print("6. Evaluating model performance...")
    metrics = predictor.evaluate_model()
    print(f"   RMSE: ${metrics['rmse']:.2f}")
    print(f"   MAE: ${metrics['mae']:.2f}")

def demo_crypto_prediction():
    """Demo cryptocurrency prediction workflow"""
    print("\n=== Cryptocurrency Prediction Demo ===")
    
    # 1. Create predictor
    print("1. Creating LSTM predictor for Bitcoin (BTC-USD)...")
    predictor = LSTMPredictor('BTC-USD', period='1y')
    
    # 2. Fetch data
    print("2. Fetching historical data...")
    if predictor.fetch_data():
        print(f"   Successfully fetched {len(predictor.data)} days of data")
    else:
        print("   Failed to fetch data")
        return
    
    # 3. Show recent prices
    print("3. Recent closing prices:")
    print(predictor.data['Close'].tail())
    
    # 4. Train model
    print("4. Training LSTM model...")
    history = predictor.train(epochs=20, batch_size=32)
    print("   Model training completed")
    
    # 5. Make prediction
    print("5. Making prediction...")
    next_day_price = predictor.predict_next_day()
    current_price = predictor.data['Close'][-1]
    
    print(f"   Current price: ${current_price:.2f}")
    print(f"   Predicted next day price: ${next_day_price:.2f}")
    
    # 6. Calculate change
    change = next_day_price - current_price
    change_percent = (change / current_price) * 100
    
    print(f"   Predicted change: ${change:.2f} ({change_percent:.2f}%)")
    
    # 7. Evaluate model
    print("6. Evaluating model performance...")
    metrics = predictor.evaluate_model()
    print(f"   RMSE: ${metrics['rmse']:.2f}")
    print(f"   MAE: ${metrics['mae']:.2f}")

def demo_data_storage():
    """Demo data storage workflow"""
    print("\n=== Data Storage Demo ===")
    
    # 1. Create data handler
    print("1. Creating data handler...")
    handler = DataHandler()
    
    # 2. Fetch and store data
    print("2. Fetching and storing Tesla data...")
    success = handler.fetch_and_store_data("TSLA", period="1mo", data_type="stock")
    if success:
        print("   Data stored successfully")
    else:
        print("   Failed to store data")
        return
    
    # 3. Retrieve data
    print("3. Retrieving stored data...")
    data = handler.get_latest_data("TSLA", days=7, data_type="stock")
    print(f"   Retrieved {len(data)} records")
    if len(data) > 0:
        print("   Sample data:")
        print(data[['date', 'close']].tail())

def main():
    """Main demo function"""
    print("Oasis - Complete Workflow Demo")
    print("=" * 50)
    
    # Run all demos
    demo_stock_prediction()
    demo_crypto_prediction()
    demo_data_storage()
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")
    print("\nTo run the full application:")
    print("1. Start the backend: python run_api.py")
    print("2. Start the frontend: cd frontend && npm start")

if __name__ == "__main__":
    main()