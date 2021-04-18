import os
import json
import requests
import pandas as pd

INSIDER_TRADING_BASE_URL = "https://www.nseindia.com/api/corporates-pit"
INSIDER_TRADING_PARAM = {
    "index": "equities",
    "from_date": "",
    "to_date": ""
}
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

def fetchEquityData(from_date,to_date, useCache=False):
    """Fetch Equity Insider Trading Data between two dates (inclusive)

    Args:
        from_date (String): From Date in form of 19-01-2021
        to_date (String): To Date in form of 21-01-2021

    Returns:
        Dict or None: If successful, dict of API response else None
    """
    PARAMS = INSIDER_TRADING_PARAM.copy()
    PARAMS["from_date"] = from_date
    PARAMS["to_date"] = to_date

    file_path = f"data/{from_date}__{to_date}.json"

    print(f"\nGetting Data from {from_date} to {to_date}")

    data = None
    if os.path.isfile(file_path) and useCache:
        print("Using cached Data")
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        sess = requests.Session()
        print("Intializing")
        r = sess.get("https://www.nseindia.com/companies-listing/corporate-filings-insider-trading", headers=HEADERS)
        print("Init Done")

        print("Fetching Data From API")
        res = sess.get(INSIDER_TRADING_BASE_URL, params=PARAMS, headers=HEADERS)
        print("Fetch Done")
        print(res.url)
        if res.status_code == 200:
            data = res.json()["data"]
            if not data:
                return None
            
            if useCache:
                print("Saving data for future use")
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    json.dump(data,f)
        else:
            return None

    df = pd.DataFrame.from_dict(data)
    df = df[df["secType"] == "Equity Shares"]
    
    numberColumns = ['secAcq','befAcqSharesNo', 'befAcqSharesPer', 'secVal','afterAcqSharesNo', 'afterAcqSharesPer']
    df[numberColumns] = df[numberColumns].apply(pd.to_numeric, errors="coerce")

    dataTimeColumns = ['acqfromDt','acqtoDt','intimDt']
    df[dataTimeColumns] = df[dataTimeColumns].apply(pd.to_datetime, errors="coerce")

    df = df[['symbol', 'company', 'acqName', 'secType', 'secAcq', 'tdpTransactionType',
    'personCategory', 'befAcqSharesNo', 'befAcqSharesPer', 'secVal',
    'afterAcqSharesNo', 'afterAcqSharesPer', 'acqfromDt', 'acqtoDt',
    'intimDt', 'acqMode']]

    return df

def fetchEquityDataForSingleDay(on_date, useCache=False):
    """Fetch Equity Insider Trading Data on given Date

    Args:
        on_date (String): Date in form of 19-01-2021

    Returns:
        Dict or None: If successful, dict of API response else None
    """
    return fetchEquityData(on_date, on_date, useCache)