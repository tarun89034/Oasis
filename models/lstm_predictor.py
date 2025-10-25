import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
# pylint: disable=import-error
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
# pylint: enable=import-error

import warnings
import os
import pickle
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore')

class LSTMPredictor:
    def __init__(self, symbol, period='2y', model_dir=None):
        """
        Initialize the Oasis LSTM Predictor
        
        Args:
            symbol (str): Stock or crypto symbol (e.g., 'AAPL', 'BTC-USD')
            period (str): Period for historical data ('1y', '2y', etc.)
            model_dir (str): Directory to save/load models
        """
        self.symbol = symbol
        self.period = period
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.data = None
        self.scaled_data = None
        self.model_dir = model_dir or os.getenv('MODEL_DIR', 'models')
        
        # Create model directory if it doesn't exist
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        
    def fetch_data(self):
        """
        Fetch historical data using yfinance
        """
        try:
            logger.info(f"Fetching data for {self.symbol} with period {self.period}")
            ticker = yf.Ticker(self.symbol)
            self.data = ticker.history(period=self.period)
            logger.info(f"Fetched {len(self.data)} records for {self.symbol}")
            return True
        except Exception as e:
            logger.error(f"Error fetching data for {self.symbol}: {e}")
            return False
    
    def prepare_data(self, lookback_days=60):
        """
        Prepare data for LSTM training
        
        Args:
            lookback_days (int): Number of days to look back for prediction
        """
        if self.data is None:
            raise ValueError("No data available. Call fetch_data() first.")
            
        # Use closing prices for prediction
        close_prices = self.data['Close'].values
        close_prices = np.array(close_prices).reshape(-1, 1)
        
        # Scale the data
        self.scaled_data = self.scaler.fit_transform(close_prices)
        
        # Create sequences for training
        X, y = [], []
        for i in range(lookback_days, len(self.scaled_data)):
            X.append(self.scaled_data[i-lookback_days:i, 0])
            y.append(self.scaled_data[i, 0])
            
        X, y = np.array(X), np.array(y)
        
        # Reshape X for LSTM input [samples, time steps, features]
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        return X, y
    
    def build_model(self, lookback_days=60):
        """
        Build the LSTM model
        
        Args:
            lookback_days (int): Number of days to look back for prediction
        """
        self.model = Sequential()
        
        # First LSTM layer
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(lookback_days, 1)))
        self.model.add(Dropout(0.2))
        
        # Second LSTM layer
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.2))
        
        # Third LSTM layer
        self.model.add(LSTM(units=50, return_sequences=False))
        self.model.add(Dropout(0.2))
        
        # Output layer
        self.model.add(Dense(units=1))
        
        # Compile the model
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
        
        return self.model
    
    def train(self, epochs=None, batch_size=None, lookback_days=None):
        """
        Train the LSTM model
        
        Args:
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
            lookback_days (int): Number of days to look back for prediction
        """
        # Use environment variables for defaults
        epochs = epochs or int(os.getenv('DEFAULT_EPOCHS', 50))
        batch_size = batch_size or int(os.getenv('DEFAULT_BATCH_SIZE', 32))
        lookback_days = lookback_days or int(os.getenv('DEFAULT_LOOKBACK_DAYS', 60))
        
        logger.info(f"Training model for {self.symbol} with {epochs} epochs, batch size {batch_size}, lookback {lookback_days}")
        
        if self.data is None:
            logger.info("Fetching data before training")
            self.fetch_data()
            
        X, y = self.prepare_data(lookback_days)
        
        if self.model is None:
            logger.info("Building model")
            self.build_model(lookback_days)
        
        # Train the model
        logger.info("Starting model training")
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            verbose=0
        )
        logger.info("Model training completed")
        
        return history
    
    def predict_next_day(self, lookback_days=60):
        """
        Predict the next day's closing price
        
        Args:
            lookback_days (int): Number of days to look back for prediction
            
        Returns:
            float: Predicted next day closing price
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
            
        if self.scaled_data is None:
            raise ValueError("No scaled data available. Call prepare_data() first.")
            
        # Get the last lookback_days of scaled data
        if len(self.scaled_data) < lookback_days:
            raise ValueError(f"Not enough data for prediction. Need at least {lookback_days} days.")
            
        last_sequence = self.scaled_data[-lookback_days:]
        last_sequence = np.reshape(last_sequence, (1, lookback_days, 1))
        
        # Predict the next value
        predicted_scaled = self.model.predict(last_sequence, verbose=0)
        
        # Inverse transform to get actual price
        predicted_price = self.scaler.inverse_transform(predicted_scaled)
        
        return predicted_price[0][0]
    
    def evaluate_model(self, lookback_days=60):
        """
        Evaluate the model performance using RMSE
        
        Args:
            lookback_days (int): Number of days to look back for prediction
            
        Returns:
            dict: Dictionary containing evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
            
        X, y = self.prepare_data(lookback_days)
        predictions = self.model.predict(X, verbose=0)
        
        # Inverse transform predictions and actual values
        predictions_actual = self.scaler.inverse_transform(predictions)
        y_actual = self.scaler.inverse_transform(y.reshape(-1, 1))
        
        # Calculate RMSE
        rmse = np.sqrt(np.mean((predictions_actual - y_actual) ** 2))
        
        # Calculate MAE
        mae = np.mean(np.abs(predictions_actual - y_actual))
        
        return {
            'rmse': rmse,
            'mae': mae
        }
    
    def save_model(self):
        """
        Save the trained model and scaler to disk
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
            
        # Create filename based on symbol and period
        model_filename = f"{self.symbol}_{self.period}.h5"
        scaler_filename = f"{self.symbol}_{self.period}_scaler.npy"
        
        # Save model
        model_path = os.path.join(self.model_dir, model_filename)
        self.model.save(model_path)
        
        # Save scaler
        scaler_path = os.path.join(self.model_dir, scaler_filename)
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Scaler saved to {scaler_path}")
    
    def load_model(self):
        """
        Load a trained model and scaler from disk
        """
        # Create filename based on symbol and period
        model_filename = f"{self.symbol}_{self.period}.h5"
        scaler_filename = f"{self.symbol}_{self.period}_scaler.npy"
        
        # Check if model file exists
        model_path = os.path.join(self.model_dir, model_filename)
        scaler_path = os.path.join(self.model_dir, scaler_filename)
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            logger.warning(f"Model files not found for {self.symbol}")
            return False
            
        # Load model
        self.model = load_model(model_path)
        
        # Load scaler
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        logger.info(f"Model loaded from {model_path}")
        logger.info(f"Scaler loaded from {scaler_path}")
        return True

# Example usage
if __name__ == "__main__":
    # Set up logging for the example
    logging.basicConfig(level=logging.INFO)
    
    # Create predictor for Tesla stock
    predictor = LSTMPredictor('TSLA', period='2y')
    
    # Fetch data
    if predictor.fetch_data():
        logger.info(f"Fetched data for {predictor.symbol}")
        logger.info(f"Data shape: {predictor.data.shape}")
        
        # Train model
        logger.info("Training model...")
        history = predictor.train(epochs=50, batch_size=32)
        
        # Predict next day
        next_day_price = predictor.predict_next_day()
        logger.info(f"Predicted next day price for {predictor.symbol}: ${next_day_price:.2f}")
        
        # Evaluate model
        metrics = predictor.evaluate_model()
        logger.info(f"Model Performance - RMSE: ${metrics['rmse']:.2f}, MAE: ${metrics['mae']:.2f}")
        
        # Save model
        try:
            predictor.save_model()
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    else:
        logger.error("Failed to fetch data")