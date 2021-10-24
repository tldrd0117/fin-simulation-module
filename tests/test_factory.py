from src.data.factory import WalletFactory
from src.data.model import CurrencyBalance, CurrencyType, MarketType, Stock, StockBalance, Wallet

# pytest -s test_factory.py
def test() -> None:
    stock = Stock(market=MarketType.KOSPI, code="005930", name="삼성전자", price="70400")
    print(stock)
    sb = StockBalance(stock=stock, count=3)
    print(sb)
    cb = CurrencyBalance(currencyType=CurrencyType.KRW, balance=10000)
    print(cb)
    wallet = Wallet(walletName="나의지갑", stockBalance=[sb], currencyBalance=[cb], date="20211024")
    print(wallet)
    print(WalletFactory.dataframe(wallet))
