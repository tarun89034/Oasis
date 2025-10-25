# Oasis - Project Summary

This document provides a comprehensive overview of the Oasis project, a full-stack web application for predicting stock and cryptocurrency prices using machine learning.

## Project Components

### 1. LSTM Prediction Model (`models/lstm_predictor.py`)

- **Purpose**: Predicts next-day prices for stocks and cryptocurrencies
- **Technology**: Python, TensorFlow/Keras, LSTM neural networks
- **Features**:
  - Fetches historical data using yfinance
  - Implements a 3-layer LSTM model with dropout regularization
  - Scales data using MinMaxScaler for optimal training
  - Provides evaluation metrics (RMSE, MAE)
  - Self-correction mechanism for model improvement

### 2. FastAPI Backend (`api/main.py`)

- **Purpose**: Exposes RESTful API endpoints for the prediction engine
- **Endpoints**:
  - `POST /predict` - Predict next day's price for a symbol
  - `GET /historical` - Get historical price data for a symbol
  - `POST /update_model` - Update/retrain the model for a symbol
- **Features**:
  - Model caching for improved performance
  - Error handling and validation
  - Automatic API documentation via Swagger UI

### 3. Data Management (`data/`)

- **Data Handler** (`data_handler.py`):
  - Fetches data using yfinance
  - Stores data in SQLite database
  - Provides historical data retrieval functions

- **Scheduler** (`scheduler.py`):
  - Periodically updates market data
  - Retrains models on a scheduled basis
  - Uses APScheduler for job scheduling

### 4. Frontend Dashboard (`frontend/`)

- **Technology**: React.js, Tailwind CSS, Chart.js
- **Components**:
  - Symbol selector for stocks and cryptocurrencies
  - Time range selection (1W, 1M, 3M, 6M, 1Y)
  - Live price charts
  - Prediction display for next day, week, and month
  - Model health panel showing accuracy metrics

### 5. Project Infrastructure

- **Requirements Management**: `requirements.txt` for Python dependencies
- **Frontend Dependencies**: `package.json` for Node.js dependencies
- **Project Documentation**: `README.md` with setup and usage instructions
- **Initialization Scripts**: Scripts to set up and run the entire application

## Implementation Details

### Machine Learning Pipeline

1. **Data Collection**: Uses yfinance to fetch historical price data
2. **Data Preprocessing**: Scales data using MinMaxScaler
3. **Feature Engineering**: Creates sequences of historical prices for LSTM input
4. **Model Training**: Trains a 3-layer LSTM neural network
5. **Evaluation**: Calculates RMSE and MAE metrics
6. **Prediction**: Predicts next-day closing prices
7. **Self-Correction**: Periodically retrains models with new data

### Backend Architecture

- **Framework**: FastAPI for high-performance API
- **Model Serving**: In-memory model caching for fast predictions
- **Data Storage**: SQLite database for historical data
- **Scheduling**: APScheduler for periodic data updates and model retraining

### Frontend Architecture

- **Framework**: React.js with functional components and hooks
- **Styling**: Tailwind CSS for responsive design
- **Visualization**: Chart.js for interactive charts
- **State Management**: React's built-in state management

## How to Run the Application

### Prerequisites

- Python 3.7+
- Node.js 14+
- pip (Python package manager)
- npm (Node.js package manager)

### Setup

1. **Initialize the project**:
   ```bash
   python init_project.py
   ```

2. **Run the backend API**:
   ```bash
   python run_api.py
   ```

3. **Run the frontend** (in a separate terminal):
   ```bash
   cd frontend
   npm start
   ```

4. **Access the application**:
   - API documentation: http://localhost:8000/docs
   - Frontend dashboard: http://localhost:3000

## Future Enhancements

1. **Advanced Models**: Implement Prophet and XGBoost models for comparison
2. **Real-time Data**: Integrate WebSocket for live price updates
3. **User Authentication**: Add user accounts and preferences
4. **Enhanced Dashboard**: Add more visualization options and technical indicators
5. **Mobile App**: Create a React Native mobile application
6. **Cloud Deployment**: Deploy to cloud platforms like AWS or Google Cloud
7. **Alert System**: Implement price alerts and notifications
8. **Portfolio Management**: Add portfolio tracking features

## Key Features Implemented

✅ LSTM model for price prediction
✅ Real-time data fetching with yfinance
✅ RESTful API with FastAPI
✅ Database storage with SQLite
✅ Interactive dashboard with React.js
✅ Model evaluation metrics (RMSE, MAE)
✅ Scheduled data updates and model retraining
✅ Responsive UI with Tailwind CSS
✅ Self-correction mechanism

## Technologies Used

- **Backend**: Python, FastAPI, TensorFlow/Keras, SQLite
- **Frontend**: React.js, Tailwind CSS, Chart.js
- **Data**: yfinance, pandas, numpy
- **Scheduling**: APScheduler
- **Development**: Vite, npm

This implementation provides a solid foundation for a stock and cryptocurrency prediction system that can be extended with additional features and models as needed.