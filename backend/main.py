from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine, Base, Company, StockData
from models import Company as CompanyModel, StockData as StockDataModel
from stock_service import populate_companies, populate_all_stock_data, get_stock_data, test_data_generation, force_populate_stock_data
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Market Dashboard API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database with sample data on startup"""
    try:
        print("Initializing database...")
        populate_companies()
        print("Companies populated successfully")
        
        # Skip data population on startup to avoid hanging
        print("Skipping data population on startup to avoid connection issues...")
        print("Use /api/populate-all-data endpoint to populate data manually")
    except Exception as e:
        print(f"Error during startup: {e}")
        print("Continuing with startup despite errors...")

@app.get("/")
async def root():
    return {"message": "Stock Market Dashboard API", "version": "1.0.0"}

@app.get("/api/companies")
async def get_companies(db: Session = Depends(get_db)):
    """Get all companies"""
    companies = db.query(Company).all()
    return [CompanyModel.from_orm(company) for company in companies]

@app.get("/api/companies/{symbol}")
async def get_company(symbol: str, db: Session = Depends(get_db)):
    """Get a specific company by symbol"""
    company = db.query(Company).filter(Company.symbol == symbol).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return CompanyModel.from_orm(company)

@app.get("/api/stocks/{symbol}")
async def get_stock_data_endpoint(symbol: str, days: int = 30, db: Session = Depends(get_db)):
    """Get stock data for a specific company with time range"""
    # Validate days parameter
    if days < 1 or days > 1825:  # Max 5 years
        raise HTTPException(status_code=400, detail="Days must be between 1 and 1825")
    
    # Check if company exists
    company = db.query(Company).filter(Company.symbol == symbol).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get stock data
    stock_data = get_stock_data(symbol, days)
    return stock_data

@app.get("/api/stocks/{symbol}/latest")
async def get_latest_stock_data(symbol: str, db: Session = Depends(get_db)):
    """Get the latest stock data for a specific company"""
    # Check if company exists
    company = db.query(Company).filter(Company.symbol == symbol).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get latest stock data
    latest_data = db.query(StockData).filter(
        StockData.company_symbol == symbol
    ).order_by(StockData.date.desc()).first()
    
    if not latest_data:
        raise HTTPException(status_code=404, detail="No stock data found")
    
    return {
        "symbol": symbol,
        "date": latest_data.date,
        "open_price": latest_data.open_price,
        "high_price": latest_data.high_price,
        "low_price": latest_data.low_price,
        "close_price": latest_data.close_price,
        "volume": latest_data.volume
    }

@app.post("/api/refresh-data")
async def refresh_stock_data(symbol: str, days: int = 30, db: Session = Depends(get_db)):
    """Refresh stock data for a specific company"""
    # Validate days parameter
    if days < 1 or days > 1825:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 1825")
    
    # Check if company exists
    company = db.query(Company).filter(Company.symbol == symbol).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Clear existing data for this symbol and time range
    from datetime import datetime, timedelta
    end_date = datetime.now()
    if days > 365:
        start_date = end_date - timedelta(weeks=min(days // 7, 260))
    else:
        start_date = end_date - timedelta(days=days)
    
    db.query(StockData).filter(
        StockData.company_symbol == symbol,
        StockData.date >= start_date
    ).delete()
    db.commit()
    
    # Get fresh data
    stock_data = get_stock_data(symbol, days)
    return {"message": f"Data refreshed for {symbol}", "data": stock_data}

@app.post("/api/populate-all-data")
async def populate_all_data():
    """Populate stock data for all companies and all time periods"""
    try:
        populate_all_stock_data()
        return {"message": "Successfully populated stock data for all companies and time periods"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error populating data: {str(e)}")

@app.get("/api/time-periods")
async def get_time_periods():
    """Get available time periods for stock data"""
    return {
        "time_periods": [
            {"days": 30, "label": "1 Month"},
            {"days": 90, "label": "3 Months"},
            {"days": 180, "label": "6 Months"},
            {"days": 365, "label": "1 Year"},
            {"days": 730, "label": "2 Years"},
            {"days": 1095, "label": "3 Years"},
            {"days": 1825, "label": "5 Years"}
        ]
    }

@app.get("/api/test-data-generation")
async def test_data_generation_endpoint():
    """Test data generation functionality"""
    try:
        test_data_generation()
        return {"message": "Data generation test completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data generation test failed: {str(e)}")

@app.get("/api/data-status")
async def get_data_status(db: Session = Depends(get_db)):
    """Get current data status for all companies"""
    companies = db.query(Company).all()
    status = []
    
    for company in companies:
        # Count data points for each time period
        time_periods = [30, 90, 180, 365, 730, 1095, 1825]
        company_status = {
            "symbol": company.symbol,
            "name": company.name,
            "data_points": {}
        }
        
        for days in time_periods:
            # Calculate expected data points
            expected_points = days if days <= 365 else min(days // 7, 260)
            
            # Count actual data points
            from datetime import datetime, timedelta
            end_date = datetime.now()
            if days > 365:
                start_date = end_date - timedelta(weeks=min(days // 7, 260))
            else:
                start_date = end_date - timedelta(days=days)
            
            actual_points = db.query(StockData).filter(
                StockData.company_symbol == company.symbol,
                StockData.date >= start_date
            ).count()
            
            company_status["data_points"][f"{days}_days"] = {
                "expected": expected_points,
                "actual": actual_points,
                "percentage": round((actual_points / expected_points * 100) if expected_points > 0 else 0, 1)
            }
        
        status.append(company_status)
    
    return {"companies": status}

@app.post("/api/force-populate/{symbol}")
async def force_populate_company_data(symbol: str, days: int = 30, db: Session = Depends(get_db)):
    """Force populate stock data for a specific company and time period"""
    # Check if company exists
    company = db.query(Company).filter(Company.symbol == symbol).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Validate days parameter
    if days < 1 or days > 1825:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 1825")
    
    try:
        force_populate_stock_data(symbol, days)
        return {"message": f"Successfully force populated data for {symbol} ({days} days)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error force populating data: {str(e)}")

@app.post("/api/populate-sample-data")
async def populate_sample_data():
    """Populate sample data for a few companies to test the system"""
    try:
        # Populate data for just a few companies with shorter time periods
        sample_companies = ["AAPL", "MSFT", "GOOGL"]
        sample_periods = [30, 90, 180]  # 1 month, 3 months, 6 months
        
        results = []
        for symbol in sample_companies:
            for days in sample_periods:
                try:
                    force_populate_stock_data(symbol, days)
                    results.append(f"✓ {symbol} ({days} days)")
                except Exception as e:
                    results.append(f"✗ {symbol} ({days} days): {str(e)}")
        
        return {
            "message": "Sample data population completed",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error populating sample data: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
