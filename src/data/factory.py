from src.data.model import Wallet
from src.util.modelToDict import modelToDict
import numpy as np
import pandas as pd

import dask.dataframe as dd
import dask.array as da
import dask.bag as db

class WalletFactory:
    @staticmethod
    def dataframe(wallet: Wallet):
        target = dict()
        target["walletName"] = wallet.walletName
        target["stockTotalBalance"] = wallet.stockTotalBalance
        target["currencyTotalBalance"] = wallet.currencyTotalBalance
        target["totalBalance"] = wallet.totalBalance
        target["date"] = wallet.date
        return pd.DataFrame([target])
        
