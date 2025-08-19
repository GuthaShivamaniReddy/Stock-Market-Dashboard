import random
from datetime import datetime, timedelta
import yfinance as yf
from database import get_db, Company, StockData

# Sample companies with more realistic data
SAMPLE_COMPANIES = [
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "description": "Designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."
    },
    {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "description": "Develops, licenses, and supports software, services, devices, and solutions worldwide."
    },
    {
        "symbol": "GOOGL",
        "name": "Alphabet Inc.",
        "sector": "Technology",
        "description": "Provides online advertising services in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America."
    },
    {
        "symbol": "AMZN",
        "name": "Amazon.com Inc.",
        "sector": "Consumer Discretionary",
        "description": "Engages in the retail sale of consumer products and subscriptions in North America and internationally."
    },
    {
        "symbol": "TSLA",
        "name": "Tesla Inc.",
        "sector": "Consumer Discretionary",
        "description": "Designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems."
    },
    {
        "symbol": "NVDA",
        "name": "NVIDIA Corporation",
        "sector": "Technology",
        "description": "Designs, develops, and manufactures computer graphics processors, chipsets, and related multimedia software."
    },
    {
        "symbol": "META",
        "name": "Meta Platforms Inc.",
        "sector": "Technology",
        "description": "Develops products that enable people to connect and share with friends and family through mobile devices, personal computers, virtual reality headsets, and wearables worldwide."
    },
    {
        "symbol": "NFLX",
        "name": "Netflix Inc.",
        "sector": "Communication Services",
        "description": "Provides entertainment services. It offers TV series, documentaries, and feature films across various genres and languages."
    },
    {
        "symbol": "JPM",
        "name": "JPMorgan Chase & Co.",
        "sector": "Financial Services",
        "description": "Operates as a financial services company worldwide. It operates through Consumer & Community Banking, Corporate & Investment Bank, Commercial Banking, and Asset & Wealth Management segments."
    },
    {
        "symbol": "JNJ",
        "name": "Johnson & Johnson",
        "sector": "Healthcare",
        "description": "Researches, develops, manufactures, and sells various products in the healthcare field worldwide."
    },
    {
        "symbol": "V",
        "name": "Visa Inc.",
        "sector": "Financial Services",
        "description": "Operates as a payments technology company worldwide. It facilitates digital payments among consumers, merchants, financial institutions, businesses, strategic partners, and government entities."
    },
    {
        "symbol": "PG",
        "name": "Procter & Gamble Co.",
        "sector": "Consumer Staples",
        "description": "Provides branded consumer packaged goods to consumers through retailers and wholesalers worldwide."
    }
]

def populate_companies():
    """Populate the database with sample companies"""
    db = next(get_db())
    
    # Check if companies already exist
    existing_companies = db.query(Company).count()
    if existing_companies > 0:
        return
    
    for company_data in SAMPLE_COMPANIES:
        company = Company(**company_data)
        db.add(company)
    
    db.commit()
    print(f"Populated {len(SAMPLE_COMPANIES)} companies")

def populate_all_stock_data():
    """Populate stock data for all companies and all time periods"""
    # Get all companies
    db = next(get_db())
    companies = db.query(Company).all()
    db.close()
    
    # Define time periods in days
    time_periods = [
        90,    # 3 months
        180,   # 6 months
        365,   # 1 year
        730,   # 2 years
        1095,  # 3 years
        1825   # 5 years
    ]
    
    print("Starting to populate stock data for all time periods...")
    
    # Process companies one by one to avoid connection pool issues
    for company in companies:
        print(f"Processing {company.symbol}...")
        for days in time_periods:
            try:
                # Use separate database session for each operation
                force_populate_stock_data(company.symbol, days)
            except Exception as e:
                print(f"Error populating data for {company.symbol} ({days} days): {e}")
    
    print("Finished populating stock data for all time periods")

def generate_mock_stock_data(symbol, days=30):
    """Generate realistic mock stock data for a given symbol and number of days"""
    # Base prices for different companies (more realistic)
    base_prices = {
        "AAPL": 150.0,
        "MSFT": 300.0,
        "GOOGL": 2800.0,
        "AMZN": 3300.0,
        "TSLA": 800.0,
        "NVDA": 400.0,
        "META": 300.0,
        "NFLX": 500.0,
        "JPM": 150.0,
        "JNJ": 170.0,
        "V": 250.0,
        "PG": 140.0
    }
    
    base_price = base_prices.get(symbol, 100.0)
    current_price = base_price
    data = []
    
    # Generate data points based on the time range
    if days <= 7:
        # For 1 week, generate daily data
        data_points = days
        volatility = 0.02  # 2% daily volatility
        interval_type = "daily"
    elif days <= 30:
        # For 1 month, generate daily data
        data_points = days
        volatility = 0.015  # 1.5% daily volatility
        interval_type = "daily"
    elif days <= 90:
        # For 3 months, generate daily data
        data_points = days
        volatility = 0.012  # 1.2% daily volatility
        interval_type = "daily"
    elif days <= 180:
        # For 6 months, generate daily data
        data_points = days
        volatility = 0.011  # 1.1% daily volatility
        interval_type = "daily"
    elif days <= 365:
        # For 1 year, generate daily data
        data_points = days
        volatility = 0.01  # 1% daily volatility
        interval_type = "daily"
    elif days <= 730:
        # For 2 years, generate weekly data
        data_points = min(days // 7, 104)  # ~104 weeks
        volatility = 0.025  # 2.5% weekly volatility
        interval_type = "weekly"
    elif days <= 1095:
        # For 3 years, generate weekly data
        data_points = min(days // 7, 156)  # ~156 weeks
        volatility = 0.03  # 3% weekly volatility
        interval_type = "weekly"
    else:
        # For 5 years, generate weekly data
        data_points = min(days // 7, 260)  # ~260 weeks
        volatility = 0.035  # 3.5% weekly volatility
        interval_type = "weekly"
    
    end_date = datetime.now()
    
    for i in range(data_points):
        if interval_type == "weekly":
            # For longer periods, use weekly intervals
            date = end_date - timedelta(weeks=data_points - i)
        else:
            # For shorter periods, use daily intervals
            date = end_date - timedelta(days=data_points - i)
        
        # Generate price movement with trend
        change_percent = random.gauss(0, volatility)
        
        # Add some trend for longer periods
        if days > 365:
            # Add slight upward trend for longer periods
            trend = 0.0005  # 0.05% weekly trend
            change_percent += trend
        
        current_price *= (1 + change_percent)
        
        # Ensure price doesn't go negative or too low
        current_price = max(current_price, base_price * 0.1)
        
        # Generate OHLC data
        if interval_type == "weekly":
            daily_volatility = volatility * 0.3  # Lower for weekly data
        else:
            daily_volatility = volatility * 0.5
        
        open_price = current_price * (1 + random.gauss(0, daily_volatility))
        high_price = max(open_price, current_price) * (1 + abs(random.gauss(0, daily_volatility)))
        low_price = min(open_price, current_price) * (1 - abs(random.gauss(0, daily_volatility)))
        close_price = current_price
        
        # Generate volume (more realistic)
        base_volume = 1000000  # 1M base volume
        volume_multiplier = random.uniform(0.5, 2.0)
        volume = int(base_volume * volume_multiplier * (1 + abs(change_percent) * 10))
        
        data.append({
            "company_symbol": symbol,
            "date": date,  # Return datetime object instead of string
            "open_price": round(open_price, 2),
            "high_price": round(high_price, 2),
            "low_price": round(low_price, 2),
            "close_price": round(close_price, 2),
            "volume": volume
        })
    
    return data

def fetch_live_stock_data(symbol, days=30):
    """Fetch live stock data using yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        
        # Determine the period based on days
        if days <= 7:
            period = "5d"
        elif days <= 30:
            period = "1mo"
        elif days <= 90:
            period = "3mo"
        elif days <= 180:
            period = "6mo"
        elif days <= 365:
            period = "1y"
        elif days <= 730:
            period = "2y"
        elif days <= 1095:
            period = "3y"
        else:
            period = "5y"
        
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
        
        data = []
        for date, row in hist.iterrows():
                    data.append({
            "company_symbol": symbol,
            "date": date,  # Return datetime object instead of string
            "open_price": round(float(row['Open']), 2),
            "high_price": round(float(row['High']), 2),
                "low_price": round(float(row['Low']), 2),
                "close_price": round(float(row['Close']), 2),
                "volume": int(row['Volume'])
            })
        
        return data
    except Exception as e:
        print(f"Error fetching live data for {symbol}: {e}")
        return None

def populate_stock_data(symbol, days=30):
    """Populate stock data for a company"""
    db = next(get_db())
    
    # Check if data already exists for this symbol and time range
    end_date = datetime.now()
    if days > 365:
        start_date = end_date - timedelta(weeks=min(days // 7, 260))
    else:
        start_date = end_date - timedelta(days=days)
    
    existing_data = db.query(StockData).filter(
        StockData.company_symbol == symbol,
        StockData.date >= start_date
    ).count()
    
    # For longer periods, we expect fewer data points (weekly vs daily)
    expected_data_points = days if days <= 365 else min(days // 7, 260)
    
    if existing_data >= expected_data_points * 0.8:  # If we have 80% of expected data
        print(f"Data already exists for {symbol} ({days} days) - {existing_data} points")
        return
    
    # Try to fetch live data first
    live_data = fetch_live_stock_data(symbol, days)
    
    if live_data:
        # Use live data
        for data_point in live_data:
            stock_data = StockData(**data_point)
            db.add(stock_data)
        print(f"Populated live stock data for {symbol} ({days} days) - {len(live_data)} points")
    else:
        # Use mock data
        mock_data = generate_mock_stock_data(symbol, days)
        for data_point in mock_data:
            stock_data = StockData(**data_point)
            db.add(stock_data)
        print(f"Populated mock stock data for {symbol} ({days} days) - {len(mock_data)} points")
    
    db.commit()

def force_populate_stock_data(symbol, days=30):
    """Force populate stock data for a company (ignores existing data)"""
    db = next(get_db())
    
    try:
        # Clear existing data for this symbol and time range
        end_date = datetime.now()
        if days > 365:
            start_date = end_date - timedelta(weeks=min(days // 7, 260))
        else:
            start_date = end_date - timedelta(days=days)
        
        # Delete existing data
        db.query(StockData).filter(
            StockData.company_symbol == symbol,
            StockData.date >= start_date
        ).delete()
        db.commit()
        
        # Try to fetch live data first
        live_data = fetch_live_stock_data(symbol, days)
        
        if live_data:
            # Use live data
            for data_point in live_data:
                stock_data = StockData(**data_point)
                db.add(stock_data)
            print(f"Force populated live stock data for {symbol} ({days} days) - {len(live_data)} points")
        else:
            # Use mock data
            mock_data = generate_mock_stock_data(symbol, days)
            for data_point in mock_data:
                stock_data = StockData(**data_point)
                db.add(stock_data)
            print(f"Force populated mock stock data for {symbol} ({days} days) - {len(mock_data)} points")
        
        db.commit()
    finally:
        db.close()

def force_populate_stock_data_with_session(symbol, days=30, db=None):
    """Force populate stock data for a company using an existing database session"""
    if db is None:
        db = next(get_db())
        should_close = True
    else:
        should_close = False
    
    try:
        # Clear existing data for this symbol and time range
        end_date = datetime.now()
        if days > 365:
            start_date = end_date - timedelta(weeks=min(days // 7, 260))
        else:
            start_date = end_date - timedelta(days=days)
        
        # Delete existing data
        db.query(StockData).filter(
            StockData.company_symbol == symbol,
            StockData.date >= start_date
        ).delete()
        db.commit()
        
        # Try to fetch live data first
        live_data = fetch_live_stock_data(symbol, days)
        
        if live_data:
            # Use live data
            for data_point in live_data:
                stock_data = StockData(**data_point)
                db.add(stock_data)
            print(f"Force populated live stock data for {symbol} ({days} days) - {len(live_data)} points")
        else:
            # Use mock data
            mock_data = generate_mock_stock_data(symbol, days)
            for data_point in mock_data:
                stock_data = StockData(**data_point)
                db.add(stock_data)
            print(f"Force populated mock stock data for {symbol} ({days} days) - {len(mock_data)} points")
        
        db.commit()
    finally:
        if should_close:
            db.close()

def get_stock_data(symbol, days=30):
    """Get stock data for a company"""
    db = next(get_db())
    
    # Calculate the start date based on days
    end_date = datetime.now()
    if days > 365:
        start_date = end_date - timedelta(weeks=min(days // 7, 260))
    else:
        start_date = end_date - timedelta(days=days)
    
    # Get existing data
    data = db.query(StockData).filter(
        StockData.company_symbol == symbol,
        StockData.date >= start_date
    ).order_by(StockData.date).all()
    
    # For longer periods, we expect fewer data points (weekly vs daily)
    expected_data_points = days if days <= 365 else min(days // 7, 260)
    
    # If no data exists or data is insufficient, populate it
    if len(data) < expected_data_points * 0.8:  # If we have less than 80% of expected data
        populate_stock_data(symbol, days)
        # Fetch the data again
        data = db.query(StockData).filter(
            StockData.company_symbol == symbol,
            StockData.date >= start_date
        ).order_by(StockData.date).all()
    
    return [{"date": item.date, "open_price": item.open_price, "high_price": item.high_price, 
             "low_price": item.low_price, "close_price": item.close_price, "volume": item.volume} 
            for item in data]

def test_data_generation():
    """Test function to verify data generation is working"""
    print("Testing data generation...")
    
    # Test mock data generation
    test_data = generate_mock_stock_data("AAPL", 30)
    print(f"Generated {len(test_data)} test data points for AAPL (30 days)")
    if test_data:
        print(f"Sample data point: {test_data[0]}")
    
    # Test database connection
    try:
        db = next(get_db())
        companies = db.query(Company).all()
        print(f"Found {len(companies)} companies in database")
        if companies:
            print(f"Sample company: {companies[0].symbol} - {companies[0].name}")
    except Exception as e:
        print(f"Database connection error: {e}")
    
    print("Data generation test completed")
