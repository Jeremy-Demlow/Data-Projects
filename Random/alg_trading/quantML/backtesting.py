import datetime as dt
import pandas as pd
from . import production


def generate_predictions(tickers, dfml, file_path, low_threshold=0.01, high_threshold=0.05):
    today = str(dt.date.today())
    pred_df = dfml[[i for i in dfml.columns if 'date' in i]].drop_duplicates()
    for ticker in tickers:
        model = production.TabularML(ticker, today, file_path)
        model.load_ml_files()
        days = model.model_specifiers['feat_days']
        feats = [f'{i}_percent_change_{days}' for i in model.model_specifiers['tickers']]

        X = model.PCA.transform(dfml[feats])
        y = model.predictor.predict(X)
        y = model.scalerML.transform(y.reshape(-1, 1))
        y = model.scalerReal.inverse_transform(y).T[0]

        pred_df[f'{ticker}_pred'] = y
        pred_df[f'{ticker}_buy'] = ((y > low_threshold) & (y < high_threshold)).astype(int)
    return pred_df


def merge_prices_and_predictions(price_df, pred_df, tickers):
    price_pivot = price_df[price_df.ticker.isin(tickers)].pivot(index='date', columns='ticker', values='close')
    price_pivot.columns = [f'{i}_close' for i in price_pivot.columns]
    price_pivot = price_pivot.reset_index()
    total = pd.merge(pred_df, price_pivot, left_on=['current_date'], right_on=['date']).drop('date', axis=1)
    price_pivot.columns = [f'{i}_fut' for i in price_pivot.columns]
    total = pd.merge(total, price_pivot, left_on=['prediction_date'], right_on=['date_fut'])
    total = total.drop(['date_fut', 'past_date'], axis=1)
    return total
