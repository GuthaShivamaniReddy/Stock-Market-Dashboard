import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
  Filler,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const StockChart = ({ stockData, company, timeRange, chartType }) => {
  if (!stockData || stockData.length === 0) {
    return (
      <div className="no-selection">
        <h3>No Data Available</h3>
        <p>No stock data available for {company.symbol}</p>
      </div>
    );
  }

  // Sort data by date
  const sortedData = [...stockData].sort((a, b) => new Date(a.date) - new Date(b.date));

  const getTimeRangeLabel = (range) => {
    switch (range) {
      case '7': return '1 Week';
      case '30': return '1 Month';
      case '90': return '3 Months';
      case '180': return '6 Months';
      case '365': return '1 Year';
      case '730': return '2 Years';
      case '1095': return '3 Years';
      case '1825': return '5 Years';
      default: return '1 Month';
    }
  };

  const getChartTypeLabel = (type) => {
    switch (type) {
      case 'line': return 'Line Chart';
      case 'candlestick': return 'Candlestick Chart';
      case 'area': return 'Area Chart';
      case 'bar': return 'Bar Chart';
      default: return 'Line Chart';
    }
  };

  // Common chart options
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 12,
          font: {
            size: 11,
            weight: '500'
          }
        }
      },
      title: {
        display: true,
        text: `${company.symbol} - ${getChartTypeLabel(chartType)} (${getTimeRangeLabel(timeRange)})`,
        font: {
          size: 13,
          weight: '600'
        },
        padding: {
          top: 8,
          bottom: 12
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
        cornerRadius: 6,
        padding: 8,
        displayColors: true,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              if (label.includes('Volume')) {
                label += new Intl.NumberFormat().format(context.parsed.y);
              } else {
                label += new Intl.NumberFormat('en-US', {
                  style: 'currency',
                  currency: 'USD',
                  minimumFractionDigits: 2
                }).format(context.parsed.y);
              }
            }
            return label;
          },
          title: function(context) {
            return `Date: ${context[0].label}`;
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Date',
          font: {
            size: 10,
            weight: '500'
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Price ($)',
          font: {
            size: 10,
            weight: '500'
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false
        },
        ticks: {
          callback: function(value) {
            return '$' + value.toFixed(2);
          }
        }
      }
    },
    elements: {
      point: {
        hoverRadius: 5,
        hoverBorderWidth: 2,
      }
    }
  };

  // Line Chart Data
  const lineChartData = {
    labels: sortedData.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Close Price',
        data: sortedData.map(item => item.close_price),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.3,
        pointRadius: 2,
        pointHoverRadius: 5,
        pointBackgroundColor: '#3b82f6',
        pointBorderColor: '#fff',
        pointBorderWidth: 1,
        fill: false,
        borderWidth: 2,
      }
    ]
  };

  // Area Chart Data
  const areaChartData = {
    labels: sortedData.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Close Price',
        data: sortedData.map(item => item.close_price),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        tension: 0.3,
        pointRadius: 2,
        pointHoverRadius: 5,
        pointBackgroundColor: '#3b82f6',
        pointBorderColor: '#fff',
        pointBorderWidth: 1,
        fill: true,
        borderWidth: 2,
      }
    ]
  };

  // Bar Chart Data
  const barChartData = {
    labels: sortedData.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Close Price',
        data: sortedData.map(item => item.close_price),
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: '#3b82f6',
        borderWidth: 1,
        borderRadius: 3,
        borderSkipped: false,
      }
    ]
  };

  // Candlestick-like Chart Data (using multiple datasets)
  const candlestickData = {
    labels: sortedData.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'High',
        data: sortedData.map(item => item.high_price),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.1,
        pointRadius: 1,
        pointHoverRadius: 3,
        borderWidth: 1,
        fill: false,
      },
      {
        label: 'Low',
        data: sortedData.map(item => item.low_price),
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.1,
        pointRadius: 1,
        pointHoverRadius: 3,
        borderWidth: 1,
        fill: false,
      },
      {
        label: 'Close',
        data: sortedData.map(item => item.close_price),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.3,
        pointRadius: 2,
        pointHoverRadius: 5,
        pointBackgroundColor: '#3b82f6',
        pointBorderColor: '#fff',
        pointBorderWidth: 1,
        borderWidth: 2,
        fill: false,
      }
    ]
  };

  // Volume Chart Data
  const volumeData = {
    labels: sortedData.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [{
      label: 'Volume',
      data: sortedData.map(item => item.volume),
      backgroundColor: 'rgba(139, 92, 246, 0.6)',
      borderColor: '#8b5cf6',
      borderWidth: 1,
      borderRadius: 3,
      borderSkipped: false,
    }]
  };

  const volumeOptions = {
    ...commonOptions,
    plugins: {
      ...commonOptions.plugins,
      title: {
        display: true,
        text: `${company.symbol} Trading Volume (${getTimeRangeLabel(timeRange)})`,
        font: {
          size: 13,
          weight: '600'
        },
        padding: {
          top: 8,
          bottom: 12
        }
      },
      legend: {
        display: false
      }
    },
    scales: {
      ...commonOptions.scales,
      y: {
        display: true,
        title: {
          display: true,
          text: 'Volume',
          font: {
            size: 10,
            weight: '500'
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false
        },
        ticks: {
          callback: function(value) {
            if (value >= 1000000) {
              return (value / 1000000).toFixed(1) + 'M';
            } else if (value >= 1000) {
              return (value / 1000).toFixed(1) + 'K';
            }
            return value;
          }
        }
      }
    }
  };

  // Render chart based on type
  const renderChart = () => {
    switch (chartType) {
      case 'line':
        return <Line data={lineChartData} options={commonOptions} />;
      case 'area':
        return <Line data={areaChartData} options={commonOptions} />;
      case 'bar':
        return <Bar data={barChartData} options={commonOptions} />;
      case 'candlestick':
        return <Line data={candlestickData} options={commonOptions} />;
      default:
        return <Line data={lineChartData} options={commonOptions} />;
    }
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '15px' }}>
      <div style={{ flex: '2', minHeight: '280px' }}>
        {renderChart()}
      </div>
      <div style={{ flex: '1', minHeight: '120px' }}>
        <Bar data={volumeData} options={volumeOptions} />
      </div>
    </div>
  );
};

export default StockChart;
