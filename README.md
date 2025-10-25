# Oasis

A full-stack web application that predicts stock and cryptocurrency prices using machine learning. The system integrates real-time data, self-correction logic, and interactive dashboards for visualization.

## Features

- **Prediction Engine**: Robust ML model to predict future stock and crypto prices using LSTM neural networks
- **Real-time Data**: Fetch live data using yfinance for stocks and ccxt for cryptocurrencies
- **Self-Correction**: Model automatically adjusts parameters based on recent real data
- **Interactive Dashboard**: Visualize historical price trends and predictions
- **API Endpoints**: RESTful API for accessing predictions and historical data

## Project Structure

```
oasis/
├── models/              # Machine learning models
├── api/                 # FastAPI backend
├── data/                # Data storage
├── frontend/            # React.js dashboard
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## LSTM Model

The LSTM (Long Short-Term Memory) model is implemented in [models/lstm_predictor.py](models/lstm_predictor.py). It uses historical price data to predict the next day's closing price.

### Key Features

- Uses yfinance to fetch historical stock and cryptocurrency data
- Implements a 3-layer LSTM neural network with dropout for regularization
- Scales data using MinMaxScaler for better training performance
- Provides evaluation metrics (RMSE, MAE) to assess model performance

## API Endpoints

The FastAPI backend provides the following endpoints:

- `POST /predict` - Predict next day's price for a symbol
- `GET /historical` - Get historical price data for a symbol
- `POST /update_model` - Update/retrain the model for a symbol

## Frontend Dashboard

The frontend is built with React.js and Tailwind CSS, featuring:

- Interactive symbol selector for stocks and cryptocurrencies
- Time range selection (1W, 1M, 3M, 6M, 1Y)
- Live price charts using Chart.js
- Prediction display for next day, week, and month
- Model health panel showing accuracy metrics

## Installation

### Backend

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the LSTM model test:
   ```bash
   python models/test_lstm.py
   ```

3. Run the API server:
   ```bash
   uvicorn api.main:app --reload
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

### Using the LSTM Model Directly

```python
from models.lstm_predictor import LSTMPredictor

# Create predictor for Tesla stock
predictor = LSTMPredictor('TSLA', period='1y')

# Fetch data and train model
predictor.fetch_data()
predictor.train(epochs=50)

# Predict next day's price
next_day_price = predictor.predict_next_day()
print(f"Predicted next day price: ${next_day_price:.2f}")
```

### Using the API

1. Start the server:
   ```bash
   uvicorn api.main:app --reload
   ```

2. Make a prediction request:
   ```bash
   curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"symbol": "TSLA", "type": "stock"}'
   ```

### Using the Frontend

1. Start both the API server and frontend development server
2. Open your browser to http://localhost:3000
3. Select a symbol and time range
4. Click "Predict Price" to see predictions

## Dependencies

### Backend

- Python 3.7+
- NumPy
- Pandas
- yfinance
- Scikit-learn
- TensorFlow/Keras
- FastAPI
- Uvicorn
- APScheduler

### Frontend

- Node.js 14+
- React.js
- Tailwind CSS
- Chart.js
- Axios

## Future Enhancements

- Implement scheduled model retraining using APScheduler
- Add support for more prediction models (Prophet, XGBoost)
- Create interactive dashboard with React.js and Chart.js
- Add database storage for historical predictions
- Implement real-time data streaming
- Add user authentication and preferences