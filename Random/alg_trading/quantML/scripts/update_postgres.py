from quantML.storage import S3
import os
import numpy as np
import pandas as pd
import psycopg2


if __name__ == '__main__':

    # download predictions
    print('Downloading File from AWS')
    bucket = 'stock-data-ml'
    pred_path = 'live/predictions/'
    pred_file = 'latest_preds.snappy.parquet'
    s3 = S3(os.environ['AWSACCESSKEYID'], os.environ['AWSSECRETKEY'])
    s3.download_file(bucket, pred_path+pred_file, pred_file)

    # load data
    print('Loading Parquet File')
    df_pred = pd.read_parquet(pred_file)
    print('Creating Stats and Summary')
    df_pred = df_pred[df_pred.prediction_date == df_pred.prediction_date.max()]
    pred_cols = [i for i in df_pred.columns if 'date' not in i and 'buy' not in i]
    tickers = [i.replace('_pred', '') for i in pred_cols]
    pred_vec = np.round(df_pred[pred_cols].to_numpy()[0], 5)
    pred_dict = dict(zip(tickers, pred_vec))
    pred_date = df_pred.prediction_date.max()

    # connect to postgres
    print('Connecting to Postgres')
    conn = psycopg2.connect(
        host=os.environ['STOCK_PGSQL_HOST'],
        database=os.environ['STOCK_PGSQL_DBNAME'],
        user=os.environ['STOCK_PGSQL_USER'],
        password=os.environ['STOCK_PGSQL_PASSWORD'])
    cur = conn.cursor()

    # update the database
    insert_statement = f"""
    insert into tabular_rebalance (prediction_date, stock_summary, days_out, model)
    values(
        date('{pred_date.date()}'),
        '{str(pred_dict).replace("'", '"')}',
        5,
        'PCA to Random Forest'
    );
    """
    print('Updating Database')
    print(insert_statement)
    cur.execute(insert_statement)

    # close the connection
    conn.commit()
    cur.close()
    print('Connection closed')
