from typing import Dict, List
from dataclasses import dataclass

from enum import Enum

class MarketType(Enum):
    KOSPI = 1
    KOSDAQ = 2

class OrderType(Enum):
    BUY = 1
    SELL = 2

class CurrencyType(Enum):
    KRW = 1

class PaymentType(Enum):
    KRW = 1
    def isCurrency(self):
        return self.value < 100


@dataclass
class Stock:
    market: MarketType
    code: str
    name: str
    price: float

@dataclass
class StockOrder:
    stock: Stock
    priceIncludedPrice: float
    fee: float
    count: int
    total: float
    orderDate: str
    orderType: OrderType
    paymentAmount: float
    paymentType: PaymentType

@dataclass
class StockBalance:
    stock: Stock
    count: int

    def __init__(self, stock: Stock, count: int) -> None:
        self.stock = stock
        self.count = count
    
    @property
    def balance(self):
        return float(self.stock.price) * int(self.count)


@dataclass
class CurrencyBalance:
    currencyType: CurrencyType
    balance: float

@dataclass
class Wallet:
    walletName: str
    stockBalance: List[StockBalance]
    currencyBalance: List[CurrencyBalance]
    date: str
    
    def __init__(self, walletName: str, stockBalance: List[StockBalance], currencyBalance: List[CurrencyBalance], date: str) -> None:
        self.walletName = walletName
        self.stockBalance = stockBalance
        self.currencyBalance = currencyBalance
        self.date = date
    
    @property
    def stockTotalBalance(self):
        val = 0
        for sb in self.stockBalance:
            val += sb.balance
        return val
    
    @property
    def currencyTotalBalance(self):
        val = 0
        for cb in self.currencyBalance:
            val += cb.balance 
        return val
    
    @property
    def totalBalance(self):
        return self.stockTotalBalance + self.currencyTotalBalance


@dataclass
class WalletHistory:
    history: List[Wallet]
        