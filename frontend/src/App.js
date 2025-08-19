import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CompanyList from './components/CompanyList';
import StockChart from './components/StockChart';
import StockInfo from './components/StockInfo';
import './App.css';

function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [stockData, setStockData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [timeRange, setTimeRange] = useState('30'); // Default to 30 days
  const [chartType, setChartType] = useState('line'); // Default to line chart

  // Fetch companies on component mount
  useEffect(() => {
    fetchCompanies();
  }, []);

  // Fetch stock data when company or time range changes
  useEffect(() => {
    if (selectedCompany) {
      fetchStockData(selectedCompany.symbol, timeRange);
    }
  }, [selectedCompany, timeRange]);

  const fetchCompanies = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/companies');
      setCompanies(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch companies');
      console.error('Error fetching companies:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStockData = async (symbol, range) => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/stocks/${symbol}?days=${range}`);
      setStockData(response.data);
      setError(null);
      setLastUpdated(new Date());
    } catch (err) {
      setError('Failed to fetch stock data');
      console.error('Error fetching stock data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCompanySelect = (company) => {
    setSelectedCompany(company);
  };

  const handleTimeRangeChange = (range) => {
    setTimeRange(range);
  };

  const handleChartTypeChange = (type) => {
    setChartType(type);
  };

  const handleRefresh = async () => {
    if (selectedCompany && !isRefreshing) {
      setIsRefreshing(true);
      await fetchStockData(selectedCompany.symbol, timeRange);
      setIsRefreshing(false);
    }
  };

  const formatLastUpdated = () => {
    if (!lastUpdated) return '';
    const now = new Date();
    const diff = now - lastUpdated;
    const minutes = Math.floor(diff / 60000);
    
    if (minutes < 1) return 'Just now';
    if (minutes === 1) return '1 minute ago';
    if (minutes < 60) return `${minutes} minutes ago`;
    
    const hours = Math.floor(minutes / 60);
    if (hours === 1) return '1 hour ago';
    if (hours < 24) return `${hours} hours ago`;
    
    return lastUpdated.toLocaleDateString();
  };

  const getTimeRangeLabel = (range) => {
    switch (range) {
      case '7': return '1W';
      case '30': return '1M';
      case '90': return '3M';
      case '180': return '6M';
      case '365': return '1Y';
      case '730': return '2Y';
      case '1095': return '3Y';
      case '1825': return '5Y';
      default: return '1M';
    }
  };

  return (
    <div className="container">
      <div className="dashboard">
        <div className="sidebar">
          <h2>📈 Stock Dashboard</h2>
          <CompanyList
            companies={companies}
            selectedCompany={selectedCompany}
            onCompanySelect={handleCompanySelect}
            loading={loading}
          />
        </div>
        
        <div className="main-content">
          {selectedCompany ? (
            <>
              {/* Charts Section - Top */}
              <div className="chart-container">
                <div className="chart-header">
                  <h1 className="chart-title">{selectedCompany.name}</h1>
                  <p className="chart-subtitle">{selectedCompany.symbol} • {selectedCompany.sector}</p>
                  
                  {/* Chart Controls */}
                  <div className="chart-controls">
                    {/* Chart Type Selector */}
                    <div className="chart-type-selector">
                      <button 
                        className={`chart-type-btn ${chartType === 'line' ? 'active' : ''}`}
                        onClick={() => handleChartTypeChange('line')}
                      >
                        Line
                      </button>
                      <button 
                        className={`chart-type-btn ${chartType === 'candlestick' ? 'active' : ''}`}
                        onClick={() => handleChartTypeChange('candlestick')}
                      >
                        Candlestick
                      </button>
                      <button 
                        className={`chart-type-btn ${chartType === 'area' ? 'active' : ''}`}
                        onClick={() => handleChartTypeChange('area')}
                      >
                        Area
                      </button>
                      <button 
                        className={`chart-type-btn ${chartType === 'bar' ? 'active' : ''}`}
                        onClick={() => handleChartTypeChange('bar')}
                      >
                        Bar
                      </button>
                    </div>

                    {/* Time Range Selector */}
                    <div className="time-range-selector">
                      <button 
                        className={`time-btn ${timeRange === '7' ? 'active' : ''}`}
                        onClick={() => handleTimeRangeChange('7')}
                      >
                        1W
                      </button>
                      <button 
                        className={`time-btn ${timeRange === '30' ? 'active' : ''}`}
                        onClick={() => handleTimeRangeChange('30')}
                      >
                        1M
                      </button>
                      <button 
                        className={`time-btn ${timeRange === '90' ? 'active' : ''}`}
                        onClick={() => handleTimeRangeChange('90')}
                      >
                        3M
                      </button>
                      <button 
                        className={`time-btn ${timeRange === '180' ? 'active' : ''}`}
                        onClick={() => handleTimeRangeChange('180')}
                      >
                        6M
                      </button>
                      <button 
                        className={`time-btn ${timeRange === '365' ? 'active' : ''}`}
                        onClick={() => handleTimeRangeChange('365')}
                      >
                        1Y
                      </button>
                      <button 
                        className={`time-btn ${timeRange === '730' ? 'active' : ''}`}
                        onClick={() => handleTimeRangeChange('730')}
                      >
                        2Y
                      </button>
                      <button 
                        className={`time-btn ${timeRange === '1095' ? 'active' : ''}`}
                        onClick={() => handleTimeRangeChange('1095')}
                      >
                        3Y
                      </button>
                      <button 
                        className={`time-btn ${timeRange === '1825' ? 'active' : ''}`}
                        onClick={() => handleTimeRangeChange('1825')}
                      >
                        5Y
                      </button>
                    </div>
                  </div>

                  {lastUpdated && (
                    <div className="last-updated">
                      <span>Last updated: {formatLastUpdated()}</span>
                      <button 
                        className={`refresh-btn ${isRefreshing ? 'spinning' : ''}`}
                        onClick={handleRefresh}
                        disabled={isRefreshing}
                        title="Refresh data"
                      >
                        🔄
                      </button>
                    </div>
                  )}
                </div>
                
                <div className="chart-wrapper">
                  {loading ? (
                    <div className="loading">
                      <div className="loading-spinner"></div>
                      <p>Loading {getTimeRangeLabel(timeRange)} stock data...</p>
                    </div>
                  ) : error ? (
                    <div className="error">
                      <div className="error-icon">⚠️</div>
                      <h3>Oops! Something went wrong</h3>
                      <p>{error}</p>
                      <button className="retry-btn" onClick={handleRefresh}>
                        Try Again
                      </button>
                    </div>
                  ) : (
                    <StockChart 
                      stockData={stockData} 
                      company={selectedCompany} 
                      timeRange={timeRange}
                      chartType={chartType}
                    />
                  )}
                </div>
              </div>

              {/* Stock Info Section - Bottom */}
              <StockInfo stockData={stockData} />
            </>
          ) : (
            <div className="chart-container">
              <div className="no-selection">
                <h2>Welcome to Stock Market Dashboard</h2>
                <p>Select a company from the sidebar to view its stock data and analytics</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
