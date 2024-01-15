from datetime import datetime
import requests
import pandas as pd
import datetime as dt
import zipfile
from io import BytesIO


header = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36",
    "Sec-Fetch-User": "?1", "Accept": "*/*", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
    }
dd_mm_yyyy = '%d-%m-%Y'

def nse_urlfetch(url):
    r_session = requests.session()
    nse_live = r_session.get("http://nseindia.com", headers=header)
    return r_session.get(url, headers=header)


def bhav_copy_equities(trade_date: str):
    """
    get nse bhav copy as per the traded date provided
    :param trade_date:
    :return: pandas dataframe
    """
    trade_date = datetime.strptime(trade_date, dd_mm_yyyy)
    url = 'https://archives.nseindia.com/content/historical/EQUITIES/'
    payload = f"{str(trade_date.strftime('%Y'))}/{str(trade_date.strftime('%b').upper())}/" \
              f"cm{str(trade_date.strftime('%d%b%Y').upper())}bhav.csv.zip"
    request_bhav = nse_urlfetch(url + payload)
    bhav_df = pd.DataFrame()
    if request_bhav.status_code == 200:
        zip_bhav = zipfile.ZipFile(BytesIO(request_bhav.content), 'r')
        for file_name in zip_bhav.filelist:
            if file_name:
                bhav_df = pd.read_csv(zip_bhav.open(file_name))
    elif request_bhav.status_code == 403:
        raise FileNotFoundError(f' Data not found, change the date...')
    bhav_df = bhav_df[['SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'TOTTRDQTY',
                       'TOTTRDVAL', 'TIMESTAMP', 'TOTALTRADES']]
    return bhav_df
