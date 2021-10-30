

from src.data.model import Order, OrderBook, OrderType, PaymentType, StockOrder, Wallet

# pytest -s test_stock.py
def test():
    wallet = Wallet("test_wallet", "20211030")
    orderBook = OrderBook(
        order=Order(1, PaymentType.KRW, 100000), 
        payment=None, 
        fee=0, 
        orderDate="20211030", 
        orderType=OrderType.DEPOSIT)
    wallet.deposit(orderBook)
    assert wallet.totalBalance == 100000
    assert wallet.stockTotalBalance == 0
    assert wallet.currencyTotalBalance == 100000

    print(wallet.totalBalance)
    print(wallet.stockTotalBalance)
    print(wallet.currencyTotalBalance)
    
    orderBook = OrderBook(
        order=StockOrder(10000, PaymentType.STOCK, 3, "kospi", "005930", "삼성전자"), 
        payment=Order(1, PaymentType.KRW, -30000), 
        fee=0, 
        orderDate="20211030", 
        orderType=OrderType.BUY)
    
    wallet.orderStockByKRW(orderBook)
    assert wallet.totalBalance == 100000
    assert wallet.stockTotalBalance == 30000
    assert wallet.currencyTotalBalance == 70000
    print(wallet.totalBalance)
    print(wallet.stockTotalBalance)
    print(wallet.currencyTotalBalance)
    print(wallet)
