


from typing import Dict
import requests
import json
import pandas as pd
import os.path

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

    def loadLocal(self) -> pd.DataFrame:
        path = f"/Users/iseongjae/Documents/PersonalProjects/fin-simulation-module/src/h5/marcap/{self.market}_{self.year}.hdf"
        if os.path.isfile(path):
            return pd.read_hdf(path, key="marcap", mode="r")
        else:
            return pd.DataFrame()
    
    def saveLocalPartitionOfYear(self, targetDf: pd.DataFrame, market: str, year: str) -> bool:
        try:
            df: pd.DataFrame = self.loadLocal(market, year)
            path = f"/Users/iseongjae/Documents/PersonalProjects/fin-simulation-module/src/h5/marcap/{market}_{year}.hdf"
            if not df.empty:
                dt: pd.DatetimeIndex = df.index.get_level_values(0).drop_duplicates()
                targetDt: pd.DatetimeIndex = targetDf.index.get_level_values(0).drop_duplicates()
                # 기존의 날짜와 비교하여 없는 부분만 concat
                diff =targetDt.difference(dt)
                resultDf: pd.DataFrame = pd.concat([df, targetDf.loc[diff]]).sort_index(level=["date","market","code"])
                resultDf.to_hdf(path, key="marcap", mode="w")
            else:
                targetDf.to_hdf(path, key="marcap", mode="w")
        except Exception as e:
            print(e)
            return False
        return True
    
    def saveLocal(self) -> bool:
        pass
        

    def loadRemote(self, isSaveLocal = True):
        res = requests.get(f"http://52.78.107.218:30004/stock/marcap?market={self.market}&startDate={self.startDate}&endDate={self.endDate}")
        obj = json.dump(res.text)
        if obj["count"] > 0:
            columns = obj["list"][0].keys()
        df = pd.DataFrame(obj["list"], columns=columns)
        df.set_index(["date", "market", "code"], inplace=True)

        if isSaveLocal:
            self.saveLocal(df, )



class DataStore:
    marcapStores: Dict[str, MarcapStore]

    def loadMarcapStores():
        pass
