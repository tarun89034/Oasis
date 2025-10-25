# Oasis - Complete File Structure

```
oasis/
├── api/
│   └── main.py                 # FastAPI backend server
├── data/
│   ├── data_handler.py         # Data fetching and storage
│   └── scheduler.py            # Scheduled data updates
├── frontend/
│   ├── index.html              # Static HTML template
│   ├── package.json            # Frontend dependencies
│   ├── vite.config.js          # Vite configuration
│   └── src/
│       ├── App.jsx             # Main React component
│       ├── App.css             # Component styling
│       ├── index.css           # Global styling
│       └── main.jsx            # React entry point
├── models/
│   ├── lstm_predictor.py       # LSTM prediction model
│   └── test_lstm.py            # LSTM model testing
├── PROJECT_SUMMARY.md          # Project overview
├── README.md                   # Setup and usage instructions
├── requirements.txt            # Python dependencies
├── demo_workflow.py            # Complete workflow demonstration
├── init_project.py             # Project initialization script
├── run_api.py                  # API server runner
├── run_full_app.py             # Full application runner
└── setup.py                    # Setup script
```

## Key Components Summary

### Machine Learning Model
- **File**: [models/lstm_predictor.py](models/lstm_predictor.py)
- **Purpose**: Predicts next-day prices using LSTM neural networks
- **Features**: Data preprocessing, model training, prediction, evaluation

### Backend API
- **File**: [api/main.py](api/main.py)
- **Purpose**: RESTful API for accessing predictions
- **Endpoints**: `/predict`, `/historical`, `/update_model`

### Data Management
- **File**: [data/data_handler.py](data/data_handler.py)
- **Purpose**: Fetch and store market data
- **Features**: SQLite database integration, data retrieval

### Frontend Dashboard
- **Files**: [frontend/src/App.jsx](frontend/src/App.jsx), [frontend/index.html](frontend/index.html)
- **Purpose**: Interactive user interface
- **Features**: Symbol selector, time range controls, charts, predictions

### Project Infrastructure
- **Files**: [requirements.txt](requirements.txt), [package.json](frontend/package.json)
- **Purpose**: Dependency management
- **Tools**: Python packages, Node.js packages

### Documentation
- **Files**: [README.md](README.md), [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Purpose**: Project documentation and instructions

### Scripts
- **Files**: [demo_workflow.py](demo_workflow.py), [init_project.py](init_project.py), [run_api.py](run_api.py)
- **Purpose**: Project setup and execution helpers