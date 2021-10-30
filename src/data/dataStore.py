


from typing import Dict
import requests
import json
import pandas as pd

class MarcapStore:
    startDate: str
    endDate: str
    market: str
    localPath: str
    remotePath: str

    def __init__(self, startDate: str, endDate: str, market: str, localPath: str, remotePath: str) -> None:
        self.startDate = startDate
        self.endDate = endDate
        self.market = market
        self.localPath = localPath
        self.remotePath = remotePath

    def loadLocal():
        pass

    def saveLocal(self, marcapDf):
        marcapDf
        

    def loadRemote(self, isSaveLocal = True):
        res = requests.get(f"http://52.78.107.218:30004/stock/marcap?market={self.market}&startDate={self.startDate}&endDate={self.endDate}")
        obj = json.dump(res.text)
        if obj["count"] > 0:
            columns = obj["list"][0].keys()
        df = pd.DataFrame(obj["list"], columns=columns)
        df.set_index(["date", "market", "code"], inplace=True)

        # if isSaveLocal:



class DataStore:
    marcapStores: Dict[str, MarcapStore]

    def loadMarcapStores():
        pass
