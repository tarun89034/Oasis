"""
Test script for the Oasis LSTM Predictor
"""
import sys
import os

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.lstm_predictor import LSTMPredictor

def test_stock_prediction():
    """Test LSTM prediction for a stock"""
    print("Testing LSTM prediction for Tesla (TSLA)")
    print("=" * 50)
    
    # Create predictor for Tesla stock
    predictor = LSTMPredictor('TSLA', period='1y')
    
    # Fetch data
    if predictor.fetch_data():
        print(f"Successfully fetched {len(predictor.data)} days of data for {predictor.symbol}")
        
        # Show last 5 days of closing prices
        print("\nRecent closing prices:")
        print(predictor.data['Close'].tail())
        
        # Train model
        print("\nTraining LSTM model...")
        history = predictor.train(epochs=30, batch_size=32)
        
        # Predict next day
        next_day_price = predictor.predict_next_day()
        current_price = predictor.data['Close'][-1]
        
        print(f"\nCurrent price: ${current_price:.2f}")
        print(f"Predicted next day price: ${next_day_price:.2f}")
        
        # Calculate predicted change
        change = next_day_price - current_price
        change_percent = (change / current_price) * 100
        
        print(f"Predicted change: ${change:.2f} ({change_percent:.2f}%)")
        
        # Evaluate model
        metrics = predictor.evaluate_model()
        print(f"\nModel Performance:")
        print(f"RMSE: ${metrics['rmse']:.2f}")
        print(f"MAE: ${metrics['mae']:.2f}")
    else:
        print("Failed to fetch data")

def test_crypto_prediction():
    """Test LSTM prediction for a cryptocurrency"""
    print("\n\nTesting LSTM prediction for Bitcoin (BTC-USD)")
    print("=" * 50)
    
    # Create predictor for Bitcoin
    predictor = LSTMPredictor('BTC-USD', period='1y')
    
    # Fetch data
    if predictor.fetch_data():
        print(f"Successfully fetched {len(predictor.data)} days of data for {predictor.symbol}")
        
        # Show last 5 days of closing prices
        print("\nRecent closing prices:")
        print(predictor.data['Close'].tail())
        
        # Train model
        print("\nTraining LSTM model...")
        history = predictor.train(epochs=30, batch_size=32)
        
        # Predict next day
        next_day_price = predictor.predict_next_day()
        current_price = predictor.data['Close'][-1]
        
        print(f"\nCurrent price: ${current_price:.2f}")
        print(f"Predicted next day price: ${next_day_price:.2f}")
        
        # Calculate predicted change
        change = next_day_price - current_price
        change_percent = (change / current_price) * 100
        
        print(f"Predicted change: ${change:.2f} ({change_percent:.2f}%)")
        
        # Evaluate model
        metrics = predictor.evaluate_model()
        print(f"\nModel Performance:")
        print(f"RMSE: ${metrics['rmse']:.2f}")
        print(f"MAE: ${metrics['mae']:.2f}")
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    test_stock_prediction()
    test_crypto_prediction()