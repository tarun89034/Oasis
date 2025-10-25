"""
FastAPI application for Oasis
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.lstm_predictor import LSTMPredictor

app = FastAPI(
    title="Oasis API",
    description="API for stock and cryptocurrency price prediction using LSTM models",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store trained models in memory
trained_models = {}

class PredictionRequest(BaseModel):
    symbol: str
    type: str  # 'stock' or 'crypto'
    period: Optional[str] = "1y"
    epochs: Optional[int] = 30

class PredictionResponse(BaseModel):
    symbol: str
    current_price: float
    predicted_price: float
    change: float
    change_percent: float
    rmse: float
    mae: float

class HistoricalDataResponse(BaseModel):
    symbol: str
    data: dict

@app.get("/")
def read_root():
    return {"message": "Welcome to Oasis API", "status": "healthy"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "oasis-api"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_price(request: PredictionRequest):
    """
    Predict the next day's price for a given symbol
    """
    try:
        logger.info(f"Predicting price for {request.symbol}")
        
        # Create a unique key for the model
        model_key = f"{request.symbol}_{request.period}"
        
        # Check if we already have a trained model
        if model_key not in trained_models:
            logger.info(f"Creating new model for {request.symbol}")
            # Create and train a new model
            predictor = LSTMPredictor(request.symbol, period=request.period or "1y")
            
            # Fetch data
            logger.info(f"Fetching data for {request.symbol}")
            if not predictor.fetch_data():
                logger.error(f"Failed to fetch data for {request.symbol}")
                raise HTTPException(status_code=400, detail=f"Failed to fetch data for {request.symbol}")
            
            # Train model
            logger.info(f"Training model for {request.symbol}")
            predictor.train(epochs=request.epochs or 30)
            
            # Store the trained model
            trained_models[model_key] = predictor
        else:
            # Use the existing trained model
            logger.info(f"Using existing model for {request.symbol}")
            predictor = trained_models[model_key]
        
        # Get current price
        if predictor.data is None or predictor.data.empty:
            logger.error(f"No data available for prediction for {request.symbol}")
            raise HTTPException(status_code=500, detail="No data available for prediction")
        current_price = predictor.data['Close'].iloc[-1]
        
        # Predict next day
        logger.info(f"Predicting next day price for {request.symbol}")
        next_day_price = predictor.predict_next_day()
        
        # Calculate change
        change = next_day_price - current_price
        change_percent = (change / current_price) * 100
        
        # Evaluate model
        logger.info(f"Evaluating model for {request.symbol}")
        metrics = predictor.evaluate_model()
        
        logger.info(f"Prediction completed for {request.symbol}")
        return PredictionResponse(
            symbol=request.symbol,
            current_price=float(current_price.iloc[0]) if hasattr(current_price, 'iloc') else float(current_price),
            predicted_price=float(next_day_price),
            change=float(change),
            change_percent=float(change_percent),
            rmse=float(metrics['rmse']),
            mae=float(metrics['mae'])
        )
    except Exception as e:
        logger.error(f"Prediction failed for {request.symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/historical")
def get_historical_data(symbol: str, range: str = "1y"):
    """
    Get historical price data for a given symbol
    """
    try:
        logger.info(f"Fetching historical data for {symbol} with range {range}")
        
        # Create predictor
        predictor = LSTMPredictor(symbol, period=range)
        
        # Fetch data
        logger.info(f"Fetching data for {symbol}")
        if not predictor.fetch_data():
            logger.error(f"Failed to fetch data for {symbol}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch data for {symbol}")
        
        # Convert to dictionary
        if predictor.data is None:
            logger.error(f"No data available for {symbol}")
            raise HTTPException(status_code=500, detail="No data available")
        data = predictor.data.reset_index().to_dict(orient='records')
        
        logger.info(f"Historical data fetched for {symbol}")
        return {
            "symbol": symbol,
            "data": data
        }
    except Exception as e:
        logger.error(f"Failed to fetch historical data for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch historical data: {str(e)}")

@app.post("/update_model")
def update_model(symbol: str, period: str = "1y", epochs: int = 30):
    """
    Update/retrain the model for a given symbol
    """
    try:
        logger.info(f"Updating model for {symbol} with period {period} and {epochs} epochs")
        
        # Create a unique key for the model
        model_key = f"{symbol}_{period}"
        
        # Create and train a new model
        predictor = LSTMPredictor(symbol, period=period or "1y")
        
        # Fetch data
        logger.info(f"Fetching data for {symbol}")
        if not predictor.fetch_data():
            logger.error(f"Failed to fetch data for {symbol}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch data for {symbol}")
        
        # Train model
        logger.info(f"Training model for {symbol}")
        predictor.train(epochs=epochs or 30)
        
        # Store the trained model
        trained_models[model_key] = predictor
        
        logger.info(f"Model updated successfully for {symbol}")
        return {
            "message": f"Model for {symbol} updated successfully",
            "symbol": symbol
        }
    except Exception as e:
        logger.error(f"Model update failed for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Model update failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=os.getenv('API_HOST', '0.0.0.0'), 
        port=int(os.getenv('API_PORT', 8000))
    )