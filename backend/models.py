from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CompanyBase(BaseModel):
    symbol: str
    name: str
    sector: str
    description: Optional[str] = None

class Company(CompanyBase):
    id: int
    
    class Config:
        from_attributes = True
        # For compatibility with older Pydantic versions
        orm_mode = True

class StockDataBase(BaseModel):
    company_symbol: str
    date: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

class StockData(StockDataBase):
    id: int
    
    class Config:
        from_attributes = True
        # For compatibility with older Pydantic versions
        orm_mode = True

class CompanyList(BaseModel):
    companies: List[Company]

class StockDataList(BaseModel):
    stock_data: List[StockData]
