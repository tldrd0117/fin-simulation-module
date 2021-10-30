import requests
import json

import pandas as pd
import os.path

import dask.dataframe as dd
import dask.array as da
import dask.bag as db
# pytest -s test_get_stock.py
def loadRemoteDataframe(startDate, endDate) :
    res = requests.get(f"http://52.78.107.218:30004/stock/marcap?market=kosdaq&startDate={startDate}&endDate={endDate}")
    obj = json.loads(res.text)
    columns = []
    assert obj["list"] != None
    assert obj["count"] != None
    if obj["count"] > 0:
        columns = obj["list"][0].keys()
    df = pd.DataFrame(obj["list"], columns=columns)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df.set_index(["date", "market", "code"], inplace=True)
    return df

def loadLocalframe(market, year):
    path = f"/Users/iseongjae/Documents/PersonalProjects/fin-simulation-module/src/h5/marcap/{market}_{year}.hdf"
    if os.path.isfile(path):
        return pd.read_hdf(path)
    else:
        return None

def saveDataframe(df):
    years = pd.DatetimeIndex(df.index.get_level_values(0)).year.drop_duplicates()
    markets = df.index.get_level_values(1).drop_duplicates()
    print(years, markets)
    for year in years:
        for market in markets:
            partDf = loadLocalframe(market, year)
            # partDf = df.loc[pd.IndexSlice[str(year), market, :]]

    # for year in years:
    # df.loc[]
    # print(df.loc["2020"])

def test():
    df = loadRemoteDataframe("20211029", "20211029")
    df2 = loadRemoteDataframe("20201029", "20201029")
    df3 = loadRemoteDataframe("20191029", "20191029")
    totalDf = pd.concat([df, df2, df3]).sort_index(level=["date","market","code"])
    saveDataframe(totalDf)
    
    # print(df.loc[df.index == ("20211029","kosdaq","000250")])
