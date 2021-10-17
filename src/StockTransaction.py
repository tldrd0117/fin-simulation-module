from typing import Dict, List

from enum import Enum

class TransactionType(Enum):
    BUY = 1
    SELL = 2

class Transaction:
    market: str
    code: str
    price: float
    priceIncludedPrice: float
    fee: float
    count: int
    total: float
    date: str
    type: TransactionType

class Stock:
    market: str
    code: str
    price: float
    count: float
    total: float

class TransactionRecord:
    transaction: Transaction
    beforeBalance: float
    afterBalance: float

class Wallet:
    name: str
    records: List[TransactionRecord]
    stocks: Dict[str, Stock]
    balance: str


class StockTransaction:
    def buy(self, wallet: Wallet, transaction: Transaction):
        record = TransactionRecord()
        record.transaction = transaction
        record.beforeBalance = wallet.balance
        record.afterBalance = wallet.balance + transaction.total
    
    def calculateStocks(self, wallet: Wallet, transaction: Transaction):
        for record in wallet.records:
            if record.transaction.type == TransactionType.BUY:
                if record.transaction.code in wallet.stocks:
                    wallet.stocks[record.transaction.code] = ""

        
    
    def sell(self, wallet: Wallet, transaction: Transaction):
        record = TransactionRecord()
        record.transaction = transaction
        record.beforeBalance = wallet.balance
        record.afterBalance = wallet.balance - transaction.total

        