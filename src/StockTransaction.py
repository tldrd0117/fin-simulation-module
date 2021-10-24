from typing import Dict, List

from enum import Enum

class MarketType(Enum):
    KOSPI = 1
    KOSDAQ = 2

class OrderType(Enum):
    BUY = 1
    SELL = 2

class CurrencyType(Enum):
    KRW = 1

class Stock:
    market: MarketType
    code: str
    name: str
    price: float

class StockOrder:
    stock: Stock
    priceIncludedPrice: float
    fee: float
    count: int
    total: float
    orderDate: str
    orderType: OrderType

class StockBalance:
    stock: str
    count: int
    balance: float

class CurrencyBalance:
    currencyType: CurrencyType
    balance: float

class Wallet:
    walletName: str
    stockBalance: List[StockBalance]
    currencyBalance: List[CurrencyBalance]
    totalBalance: float

class WalletHistory:
    history: List[Wallet]



        
    

        