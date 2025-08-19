import React from 'react';

const StockInfo = ({ stockData }) => {
  if (!stockData || stockData.length === 0) {
    return null;
  }

  // Sort data by date to get latest and earliest data
  const sortedData = [...stockData].sort((a, b) => new Date(a.date) - new Date(b.date));
  const latestData = sortedData[sortedData.length - 1];
  const earliestData = sortedData[0];

  // Calculate metrics
  const currentPrice = latestData.close_price;
  const previousPrice = earliestData.close_price;
  const priceChange = currentPrice - previousPrice;
  const priceChangePercent = ((priceChange / previousPrice) * 100).toFixed(2);
  const isPositive = priceChange >= 0;

  // Calculate 30-day high and low
  const highPrices = sortedData.map(item => item.high_price);
  const lowPrices = sortedData.map(item => item.low_price);
  const thirtyDayHigh = Math.max(...highPrices);
  const thirtyDayLow = Math.min(...lowPrices);

  // Calculate average volume
  const volumes = sortedData.map(item => item.volume);
  const averageVolume = Math.round(volumes.reduce((sum, vol) => sum + vol, 0) / volumes.length);

  // Calculate volatility (standard deviation of returns)
  const returns = sortedData.slice(1).map((item, index) => {
    const prevPrice = sortedData[index].close_price;
    return ((item.close_price - prevPrice) / prevPrice) * 100;
  });
  const meanReturn = returns.reduce((sum, ret) => sum + ret, 0) / returns.length;
  const variance = returns.reduce((sum, ret) => sum + Math.pow(ret - meanReturn, 2), 0) / returns.length;
  const volatility = Math.sqrt(variance).toFixed(2);

  return (
    <div className="stock-info">
      <div className="info-card">
        <div className="info-label">Current Price</div>
        <div className="info-value">
          ${currentPrice.toFixed(2)}
        </div>
      </div>
      
      <div className="info-card">
        <div className="info-label">30-Day Change</div>
        <div className={`info-value ${isPositive ? 'positive' : 'negative'}`}>
          {isPositive ? '+' : ''}{priceChange.toFixed(2)} ({isPositive ? '+' : ''}{priceChangePercent}%)
        </div>
      </div>
      
      <div className="info-card">
        <div className="info-label">30-Day High</div>
        <div className="info-value">
          ${thirtyDayHigh.toFixed(2)}
        </div>
      </div>
      
      <div className="info-card">
        <div className="info-label">30-Day Low</div>
        <div className="info-value">
          ${thirtyDayLow.toFixed(2)}
        </div>
      </div>
      
      <div className="info-card">
        <div className="info-label">Avg Volume</div>
        <div className="info-value">
          {new Intl.NumberFormat().format(averageVolume)}
        </div>
      </div>
      
      <div className="info-card">
        <div className="info-label">Volatility</div>
        <div className="info-value">
          {volatility}%
        </div>
      </div>
    </div>
  );
};

export default StockInfo;
