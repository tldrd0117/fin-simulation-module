from typing import Any, Dict, List
from dataclasses import dataclass

from enum import Enum
import uuid

class MarketType(Enum):
    KOSPI = 1
    KOSDAQ = 2

class OrderType(Enum):
    BUY = 1
    SELL = 2
    DEPOSIT = 3

class CurrencyType(Enum):
    KRW = 1
    USD = 2

class PaymentType(Enum):
    STOCK = 1000
    KRW = 2000
    USD = 2001
    def isCurrency(self):
        return self.value >= 2000


@dataclass
class Order:
    orderAmount: float
    orderAmountType: PaymentType
    count: int

@dataclass
class StockOrder(Order):
    market: MarketType
    code: str
    name: str

@dataclass
class Payment:
    paymentAmount: float
    paymentAmountType: PaymentType
    count: int

@dataclass
class OrderBook:
    order: Order
    payment: Payment
    fee: float
    orderDate: str
    orderType: OrderType
    orderKey: str

    def __init__(self, order: Order, payment: Payment, fee: float) -> None:
        self.order = order
        self.payment = payment
        self.fee = fee
        self.orderKey = uuid.uuid1()


@dataclass
class StockBalance:
    stock: StockOrder
    count: int
    def __init__(self, stock: StockOrder, count: int) -> None:
        self.stock = stock
        self.count = count
    
    @property
    def balance(self):
        return float(self.stock.price) * int(self.count)


#1달러당 1000원이면 stdCurrencyType는 KRW targetCurrencyType은 USD amount는 1000
@dataclass
class ExchangeRate:
    stdCurrencyType: CurrencyType
    targetCurrencyType: CurrencyType
    amount: float


@dataclass
class CurrencyBalance:
    currencyType: CurrencyType
    balance: float
    
    def getValue(self, exchangeRate: ExchangeRate):
        if exchangeRate.targetCurrencyType != self.currencyType:
            print("다른 통화타입 입니다")
            return
        return exchangeRate.amount * self.balance


@dataclass
class Wallet:
    walletName: str
    orderBooks: List[OrderBook]
    stockBalance: Dict[str, StockOrder]
    currencyBalance: Dict[str, Payment]
    date: str
    standardCurrency: CurrencyType.KRW
    
    def __init__(self, walletName: str, date: str) -> None:
        self.walletName = walletName
        self.orderBooks = []
        self.stockBalance = {}
        self.currencyBalance = {}
        self.date = date
    
    @property
    def stockTotalBalance(self):
        val = 0
        for sb in self.stockBalance:
            val += self.stockBalance[sb].orderAmount * self.stockBalance[sb].count
        return val
    
    @property
    def currencyTotalBalance(self):
        val = 0
        for cb in self.currencyBalance:
            val += self.currencyBalance[cb].paymentAmount * self.currencyBalance[cb].count 
        return val
    
    @property
    def totalBalance(self):
        return self.stockTotalBalance + self.currencyTotalBalance
    

    def deposit(self, orderBook: OrderBook):
        if orderBook.orderType != orderBook.orderType.DEPOSIT:
            print("입금 주문이 아닙니다")
            return
        if orderBook.order.orderAmountType.isCurrency():
            self.currencyBalance[orderBook.orderKey] = orderBook.order
        else:
            self.stockBalance[orderBook.orderKey] = orderBook.order
    
    def orderStockByKRW(self, orderBook: OrderBook):
        if orderBook.order.orderAmountType != PaymentType.STOCK or not orderBook.payment.paymentAmountType.isCurrency():
            print("주식 매수 주문이 아닙니다")
            return
        if orderBook.payment.paymentAmountType != PaymentType.KRW:
            print("원화 주문이 아닙니다")
            return
        if self.currencyTotalBalance < orderBook.payment.paymentAmount:
            print("잔고가 부족합니다")
            return
        
        self.stockBalance[orderBook.orderKey] = orderBook.order
        if orderBook.orderType == orderBook.orderType.SELL and orderBook.payment.paymentAmount > 0:
            orderBook.payment.paymentAmount = - orderBook.payment.paymentAmount
        self.currencyBalance[orderBook.orderKey] = orderBook.payment
        self.orderBooks.append(orderBook)




        