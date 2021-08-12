import pandas as pd
import requests
import bs4 as bs
import pandas_datareader.data as web
import datetime as dt
import os

from quantML import storage
from quantML import preprocess
from quantML.utils import ParseYaml
from quantML import static_files

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_prices(ticker_list, start, stop, price_types=['Close'], logger=logger):
    """scrapes prices given a ticker list and a time period

    Args:
        ticker_list (list): stock tickers
        start (str): starting date
        stop (str): stoping date

    Returns:
        df: pandas dataframe for prices
    """

    price_array = []
    num = 1
    total = len(ticker_list)
    for stock in ticker_list:
        logger.info(f'Scraping {stock} - {num} out of {total} tickers')
        try:
            price_array.append(web.DataReader(stock, 'yahoo', start, stop))
        except:  # noqa
            price_array.append('NA')
        num += 1
    price_df = dict(zip(ticker_list, price_array))
    dels = []
    for key in price_df.keys():
        if type(price_df[key]) == str:
            dels.append(key)
    for key in dels:
        price_df.pop(key, None)
    price_df = pd.concat(price_df)
    price_df = price_df[['Close']].reset_index()
    price_df.columns = ['ticker', 'date'] + [i.lower() for i in ['Close']]
    return price_df


def get_sp500_tickers():
    """scrapes the s and p 500 list from wikipedia

    Returns:
        list: list of tickers
    """
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text[:-1]
        tickers.append(ticker)
    return tickers


def daily_scrape():

    # load tickers from static files
    path = os.path.abspath(static_files.__path__[0]) + '/models.yml'
    model_yaml = ParseYaml(path)
    tickers = model_yaml.get_yaml(['tabularML', 'tickers'])

    # scrape prices
    stop = str(dt.datetime.today().date())
    start = str(dt.datetime.today().date() - dt.timedelta(days=28))
    price_df = get_prices(tickers,
                          start,
                          stop,
                          price_types=['Close'],
                          logger=logger)

    # generate features
    full_df = preprocess.create_feats_and_preds(price_df, feat_days=5, pred_days=5)
    dfml = preprocess.generate_daily_matrix(full_df, feat_days=5)

    # save files
    feature_file_name_local = 'featureDF.snappy.parquet'
    price_file_name_local = 'priceDF.snappy.parquet'
    dfml.to_parquet(feature_file_name_local)
    price_df.to_parquet(price_file_name_local)

    # push to s3
    feature_file_name_s3 = 'live/features/featureDF.snappy.parquet'
    price_file_name_s3 = 'live/prices/featureDF.snappy.parquet'
    s3 = storage.S3(os.environ['AWSACCESSKEYID'], os.environ['AWSSECRETKEY'])
    s3.upload_file(feature_file_name_local, 'stock-data-ml', feature_file_name_s3)
    s3.upload_file(price_file_name_local, 'stock-data-ml', price_file_name_s3)

    # unlink
    os.unlink(feature_file_name_local)
    os.unlink(price_file_name_local)
