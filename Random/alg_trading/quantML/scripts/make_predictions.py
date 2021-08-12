from quantML.storage import S3
from quantML import backtesting
import os
import pandas as pd


if __name__ == '__main__':

    # download models
    bucket = 'stock-data-ml'
    model_path = 'modelfiles/tabularML/'
    s3 = S3(os.environ['AWSACCESSKEYID'], os.environ['AWSSECRETKEY'])
    s3.download_directory(bucket, model_path)

    # download feature set
    feature_file = 'live/features/featureDF.snappy.parquet'
    s3.download_file(bucket, feature_file, feature_file)

    # load data
    dfml = pd.read_parquet(feature_file)

    # make prediction dataframe
    tickers = ['HUM', 'JBHT', 'JNJ', 'LB', 'GPC', 'LH', 'LEG', 'FOXA', 'PVH',
               'WMT', 'KO', 'PNW', 'FB', 'F', 'CME', 'WMB', 'AVB', 'BR', 'GOOGL',
               'ORLY', 'SYY', 'INFO', 'KMI', 'GE', 'SCHW', 'MSFT', 'MRK', 'IP',
               'RTX', 'AVY']
    low_threshold = 0.02
    high_threshold = 0.1
    pred_df = backtesting.generate_predictions(tickers,
                                               dfml,
                                               model_path[:-1],
                                               low_threshold=low_threshold,
                                               high_threshold=high_threshold,)
    pred_df = pred_df.drop(['current_date', 'past_date'], axis=1)

    # save out dataframe
    pred_file = 'latest_preds.snappy.parquet'
    pred_df.to_parquet(pred_file)

    # push to S3
    s3.upload_file(pred_file, bucket, f'live/predictions/{pred_file}')
