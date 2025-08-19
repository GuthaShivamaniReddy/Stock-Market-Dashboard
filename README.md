# 📈 Stock Market Dashboard

A modern, responsive web application for visualizing stock market data with real-time charts and comprehensive analytics.

## 🚀 Features

### Frontend

- **Modern UI Design**: Clean, responsive interface with gradient backgrounds and smooth animations
- **Company List**: Scrollable sidebar with 12+ major companies (Apple, Microsoft, Google, etc.)
- **Interactive Charts**:
  - Line charts showing close, high, and low prices
  - Bar charts displaying trading volume
  - Hover tooltips with detailed information
- **Stock Analytics**:
  - Current price and 30-day change
  - 30-day high/low prices
  - Average trading volume
  - Volatility calculations
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### Backend

- **FastAPI REST API**: High-performance Python backend
- **SQLite Database**: Lightweight data storage with SQLAlchemy ORM
- **Stock Data**:
  - Mock data generation for demonstration
  - Optional live data fetching via yfinance
  - 30-day historical data for each company
- **CORS Support**: Cross-origin requests enabled for frontend integration

## 🛠️ Technology Stack

### Backend

- **Python 3.8+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - Database ORM
- **yfinance** - Yahoo Finance data fetching
- **SQLite** - Database
- **Uvicorn** - ASGI server

### Frontend

- **React 18** - UI framework
- **Chart.js** - Charting library
- **Axios** - HTTP client
- **CSS3** - Modern styling with gradients and animations

## 📦 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r ../requirements.txt
   ```

3. **Run the FastAPI server:**

   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

3. **Start the React development server:**

   ```bash
   npm start
   ```

   The application will open at `http://localhost:3000`

## 🎯 Usage

1. **Start both servers** (backend on port 8000, frontend on port 3000)
2. **Open your browser** and navigate to `http://localhost:3000`
3. **Select a company** from the left sidebar to view its stock data
4. **Explore the charts** and analytics for detailed insights

## 📊 API Endpoints

### Companies

- `GET /api/companies` - Get all companies
- `GET /api/companies/{symbol}` - Get specific company details

### Stock Data

- `GET /api/stocks/{symbol}` - Get stock data for a company (default: 30 days)
- `GET /api/stocks/{symbol}?days=60` - Get stock data for custom period
- `GET /api/stocks/{symbol}/latest` - Get latest stock data

### Data Management

- `POST /api/refresh-data` - Refresh stock data (mock data)
- `POST /api/refresh-data?use_live_data=true` - Refresh with live data

## 🎨 UI Features

### Design Highlights

- **Gradient Backgrounds**: Modern purple-blue gradient theme
- **Glass Morphism**: Semi-transparent cards with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Grid**: Adapts to different screen sizes
- **Interactive Elements**: Clickable company list with active states

### Chart Features

- **Multi-line Charts**: Close, high, and low prices
- **Volume Bars**: Trading volume visualization
- **Interactive Tooltips**: Detailed information on hover
- **Responsive Charts**: Automatically resize with container
- **Professional Styling**: Clean, financial-grade appearance

## 🔧 Configuration

### Backend Configuration

- Database: SQLite (file: `stock_dashboard.db`)
- Default data: Mock data (can be switched to live data)
- CORS: Enabled for all origins (development)

### Frontend Configuration

- API proxy: Configured to `http://localhost:8000`
- Chart options: Customizable via Chart.js configuration
- Responsive breakpoints: Mobile-first design

## 📈 Sample Companies

The application includes data for 12 major companies:

- **Technology**: Apple (AAPL), Microsoft (MSFT), Google (GOOGL), NVIDIA (NVDA)
- **E-commerce**: Amazon (AMZN)
- **Automotive**: Tesla (TSLA)
- **Financial**: JPMorgan Chase (JPM), Visa (V)
- **Healthcare**: Johnson & Johnson (JNJ), UnitedHealth (UNH)
- **Retail**: Walmart (WMT)
- **Consumer Goods**: Procter & Gamble (PG)

## 🚀 Deployment

### Backend Deployment

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Serve static files
npx serve -s build
```

## 🔮 Future Enhancements

- [ ] Real-time data updates
- [ ] Additional chart types (candlestick, technical indicators)
- [ ] User authentication and watchlists
- [ ] News feed integration
- [ ] Portfolio tracking
- [ ] Export functionality
- [ ] Dark/light theme toggle
