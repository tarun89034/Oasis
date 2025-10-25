import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedSymbol, setSelectedSymbol] = useState('TSLA');
  const [assetType, setAssetType] = useState('stock');
  const [timeRange, setTimeRange] = useState('1M');
  const [predictionData, setPredictionData] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Mock data for demonstration
  const symbols = {
    stock: [
      { value: 'TSLA', label: 'Tesla' },
      { value: 'AAPL', label: 'Apple' },
      { value: 'GOOGL', label: 'Google' },
      { value: 'MSFT', label: 'Microsoft' }
    ],
    crypto: [
      { value: 'BTC-USD', label: 'Bitcoin' },
      { value: 'ETH-USD', label: 'Ethereum' },
      { value: 'ADA-USD', label: 'Cardano' }
    ]
  };

  // Mock prediction data
  const mockPredictionData = {
    symbol: 'TSLA',
    current_price: 256.42,
    predicted_price: 261.25,
    change: 4.83,
    change_percent: 1.89,
    rmse: 2.35,
    mae: 1.82
  };

  // Mock historical data
  const mockHistoricalData = [
    { date: '2025-10-18', price: 245.20 },
    { date: '2025-10-19', price: 248.50 },
    { date: '2025-10-20', price: 252.30 },
    { date: '2025-10-21', price: 249.80 },
    { date: '2025-10-22', price: 253.40 },
    { date: '2025-10-23', price: 255.60 },
    { date: '2025-10-24', price: 254.20 },
    { date: '2025-10-25', price: 256.42 }
  ];

  useEffect(() => {
    const fetchHistoricalData = async () => {
      try {
        const response = await axios.get('/api/historical', {
          params: {
            symbol: selectedSymbol,
            range: timeRange.toLowerCase()
          }
        });
        setHistoricalData(response.data.data);
      } catch (error) {
        console.error('Error fetching historical data:', error);
        // Fallback to mock data
        setHistoricalData(mockHistoricalData);
      }
    };
    
    fetchHistoricalData();
  }, [selectedSymbol, timeRange]);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/predict', {
        symbol: selectedSymbol,
        type: assetType
      });
      setPredictionData(response.data);
    } catch (error) {
      console.error('Error fetching prediction:', error);
      alert('Error fetching prediction. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRefreshModel = async () => {
    try {
      await axios.post('/api/update_model', null, {
        params: {
          symbol: selectedSymbol,
          period: '1y',
          epochs: 30
        }
      });
      alert('Model refresh completed successfully');
    } catch (error) {
      console.error('Error refreshing model:', error);
      alert('Error refreshing model. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-12">
          <h1 className="text-4xl font-bold text-center mb-2">Oasis</h1>
          <p className="text-xl text-center text-gray-400">Stock & Cryptocurrency Price Prediction</p>
        </header>

        {/* Main Dashboard */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Controls */}
          <div className="lg:col-span-1 space-y-8">
            {/* Symbol Selector */}
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <h2 className="text-2xl font-bold mb-4">Symbol Selector</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Asset Type</label>
                  <div className="flex space-x-2">
                    <button 
                      className={`flex-1 py-2 px-4 rounded-lg transition ${assetType === 'stock' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
                      onClick={() => setAssetType('stock')}
                    >
                      Stock
                    </button>
                    <button 
                      className={`flex-1 py-2 px-4 rounded-lg transition ${assetType === 'crypto' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
                      onClick={() => setAssetType('crypto')}
                    >
                      Crypto
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Select Symbol</label>
                  <select 
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={selectedSymbol}
                    onChange={(e) => setSelectedSymbol(e.target.value)}
                  >
                    {symbols[assetType].map(symbol => (
                      <option key={symbol.value} value={symbol.value}>
                        {symbol.value} - {symbol.label}
                      </option>
                    ))}
                  </select>
                </div>
                <button 
                  className="w-full bg-blue-600 hover:bg-blue-700 py-2 px-4 rounded-lg transition flex items-center justify-center"
                  onClick={handlePredict}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Predicting...
                    </>
                  ) : (
                    'Predict Price'
                  )}
                </button>
              </div>
            </div>

            {/* Time Range Selector */}
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <h2 className="text-2xl font-bold mb-4">Time Range</h2>
              <div className="grid grid-cols-3 gap-2">
                {['1W', '1M', '3M', '6M', '1Y', 'All'].map(range => (
                  <button
                    key={range}
                    className={`py-2 px-4 rounded-lg transition ${timeRange === range ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}
                    onClick={() => setTimeRange(range)}
                  >
                    {range}
                  </button>
                ))}
              </div>
            </div>

            {/* Model Health Panel */}
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <h2 className="text-2xl font-bold mb-4">Model Health</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span>Accuracy</span>
                  <span className="font-mono">87.5%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>RMSE</span>
                  <span className="font-mono">2.35</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>MAE</span>
                  <span className="font-mono">1.82</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>Last Updated</span>
                  <span className="font-mono">2025-10-25</span>
                </div>
                <button 
                  className="w-full bg-green-600 hover:bg-green-700 py-2 px-4 rounded-lg transition mt-4 flex items-center justify-center"
                  onClick={handleRefreshModel}
                >
                  <i className="fas fa-sync-alt mr-2"></i>Refresh Model
                </button>
              </div>
            </div>
          </div>

          {/* Right Column - Charts and Predictions */}
          <div className="lg:col-span-2 space-y-8">
            {/* Live Chart */}
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Price Chart</h2>
                {predictionData && (
                  <div className="text-right">
                    <div className="text-2xl font-bold">${predictionData.current_price}</div>
                    <div className={`flex items-center ${predictionData.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                      {predictionData.change >= 0 ? '+' : ''}{predictionData.change_percent.toFixed(2)}% 
                      <i className={`fas ml-1 ${predictionData.change >= 0 ? 'fa-arrow-up' : 'fa-arrow-down'}`}></i>
                    </div>
                  </div>
                )}
              </div>
              <div className="h-80 bg-gray-700 rounded-lg flex items-center justify-center">
                <p>Chart visualization would appear here</p>
              </div>
            </div>

            {/* Prediction Display */}
            <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
              <h2 className="text-2xl font-bold mb-4">Price Prediction</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-700 rounded-lg p-4 text-center">
                  <div className="text-gray-400">Next Day</div>
                  <div className="text-2xl font-bold text-green-500">$261.25</div>
                  <div className="text-green-500">+1.89%</div>
                </div>
                <div className="bg-gray-700 rounded-lg p-4 text-center">
                  <div className="text-gray-400">Next Week</div>
                  <div className="text-2xl font-bold text-green-500">$272.80</div>
                  <div className="text-green-500">+6.4%</div>
                </div>
                <div className="bg-gray-700 rounded-lg p-4 text-center">
                  <div className="text-gray-400">Next Month</div>
                  <div className="text-2xl font-bold text-red-500">$245.60</div>
                  <div className="text-red-500">-4.2%</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500">
          <p>Oasis - Real-time Stock & Cryptocurrency Price Prediction</p>
        </footer>
      </div>
    </div>
  );
}

export default App;