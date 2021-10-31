import requests
import json

import pandas as pd
import numpy as np
import os.path

import dask.dataframe as dd
import dask.array as da
import dask.bag as db
import pathlib


basePath = pathlib.Path('../src/h5/marcap')


# pytest -s test_get_stock.py
def loadRemoteDataframe(market: str, startDate: str, endDate: str) -> dd.DataFrame :
    res = requests.get(f"http://52.78.107.218:30004/stock/marcap?market={market}&startDate={startDate}&endDate={endDate}")
    obj = json.loads(res.text)
    columns = []
    assert obj["list"] != None
    assert obj["count"] != None
    if obj["count"] > 0:
        columns = obj["list"][0].keys()
    df = pd.DataFrame(obj["list"], columns=columns)
    df = dd.from_pandas(df, npartitions=100)
    df["date"] = dd.to_datetime(df["date"], format="%Y%m%d")
    # df = df.set_index(["date", "market", "code"], sorted=True)
    return df

def loadLocalDataframe(market: str, year: str) -> dd.DataFrame:
    path = f"{basePath.resolve()}/{market}_{year}.hdf"
    if os.path.isfile(path):
        return dd.read_hdf(path, key="marcap", mode="r")
    else:
        return dd.from_pandas(pd.DataFrame(), npartitions=1)

def saveLocalDataframe(targetDf: dd.DataFrame, market: str, year: str) -> bool:
    try:
        df = loadLocalDataframe(market, year)
        path = f"{basePath.resolve()}/{market}_{year}.hdf"
        if len(df) > 0:
            print(df)
            dt = df["date"].drop_duplicates().map_partitions(np.asarray, dtype=np.datetime64)
            targetDt = targetDf["date"].drop_duplicates().map_partitions(np.asarray, dtype=np.datetime64)
            # 기존의 날짜와 비교하여 없는 부분만 concat
            diff = np.setdiff1d(targetDt, dt)
            resultDf = dd.concat([df, targetDf[targetDf["date"].isin(diff)]]).map_partitions(lambda df: df.sort_values(['date', 'market','code']))
            resultDf.to_hdf(path, key="marcap", mode="w", min_itemsize=100)
        else:
            targetDf.to_hdf(path, key="marcap", mode="w", min_itemsize=100)
    except Exception as e:
        print(e)
        return False
    return True

    

def saveDataframe(df: dd.DataFrame):
    df = df.persist()
    years = df["date"].dt.year.drop_duplicates()
    markets = df["market"].drop_duplicates()

    for year in years:
        for market in markets:
            partDf = df[df["date"].dt.year == year][df["market"]==market]
            saveLocalDataframe(partDf, market, year)

    # for year in years:
    # df.loc[]
    # print(df.loc["2020"])

def test():
    # print(loadLocalDataframe("kosdaq", "2019").compute())
    # print(loadLocalDataframe("kosdaq", "2020").compute())
    print(loadLocalDataframe("kosdaq", "2021").compute())
    # print(loadLocalDataframe("kospi", "2019").compute())
    # print(loadLocalDataframe("kospi", "2020").compute())
    # print(loadLocalDataframe("kospi", "2021").compute())

    # df = loadRemoteDataframe("kosdaq", "20211023", "20211025")
    # df2 = loadRemoteDataframe("kosdaq", "20201027", "20201029")
    # df3 = loadRemoteDataframe("kosdaq", "20191027", "20191029")
    # df4 = loadRemoteDataframe("kospi", "20211027", "20211029")
    # df5 = loadRemoteDataframe("kospi", "20201027", "20201029")
    # df6 = loadRemoteDataframe("kospi", "20191027", "20191029")
    # totalDf = dd.concat([df]).map_partitions(lambda df: df.sort_values(['date', 'market','code']))
    # saveDataframe(totalDf)
    
    # print(df.loc[df.index == ("20211029","kosdaq","000250")])
