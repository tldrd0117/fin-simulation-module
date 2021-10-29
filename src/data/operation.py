from src.data.model import PaymentType, StockBalance, StockOrder, Wallet
from src.util.dateUtil import currentDate

class StockOperation:
    @staticmethod
    def buy(wallet: Wallet, stockOrder: StockOrder):
        wallet.date = currentDate()
        if wallet.totalBalance < stockOrder.paymentAmount:
            print("잔고 부족")
            return False
        wallet
        sb = StockBalance(stockOrder.stock, stockOrder.count)
        wallet.stockBalance.append(sb)

