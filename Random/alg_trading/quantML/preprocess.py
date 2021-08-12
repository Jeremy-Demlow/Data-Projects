import pandas as pd


def price_n_days_out(price_df, days=5, percent=True):
    """labels prices n days out given a pricing dataframe with
    ticker, date, and price

    Args:
        price_df (df): pricing dataframe
        days (int, optional): number of days out. Defaults to 5.

    Returns:
        price_df: dataframe with prediction labels
    """
    preds = []
    for ticker in price_df.ticker.unique():
        shift_df = price_df[price_df.ticker == ticker].shift(-days)
        shift_df.columns = ['ticker', 'prediction_date', f'price_{days}_out']
        preds.append(shift_df)
    preds = pd.concat(preds)

    price_df = pd.merge(price_df, preds[['prediction_date', f'price_{days}_out']],
                        left_index=True,
                        right_index=True).dropna()
    price_df[f'percent_{days}_out'] = (price_df[f'price_{days}_out'] - price_df['close']) / price_df['close']
    return price_df


def create_feats_and_preds(price_df, feat_days, pred_days):
    """creates a feature and label dataframe for machine learning

    Args:
        price_df (df): pricing information with ticker, date, and price
        feat_days (int): number of feature days
        pred_days (int): number of days after feature days to predict out

    Returns:
        df: ml feature, label dataframe
    """

    # create shifted percent features
    df_feats = price_n_days_out(price_df, days=feat_days)
    df_help = df_feats.copy()[['ticker', 'prediction_date', f'price_{feat_days}_out']]
    df_help.columns = ['ticker', 'date', 'close']
    df_preds = price_n_days_out(df_help, days=pred_days)

    # do some cleaning
    full_df = pd.merge(df_feats, df_preds, left_on=['ticker', 'prediction_date'], right_on=['ticker', 'date'])
    full_df.columns = ['ticker', 'past_date', 'past_close', 'current_date', 'current_price',
                       'percent_change_feat', 'date_y', 'close_y', 'prediction_date',
                       'price_5_out_y', 'percent_change_pred']
    full_df = full_df[['ticker', 'past_date', 'current_date', 'prediction_date',
                       'percent_change_feat', 'percent_change_pred']]
    return full_df


def generate_ml_matrix(full_df, pred_ticker, feat_days):
    """generates an ml matrix with features based on all tickers

    Args:
        full_df (df): all features
        pred_ticker (string): prediction stock
        feat_days (int): number of feature days in change

    Returns:
        df: machine learning dataframe with dates
    """

    feature_tickers = [i for i in full_df.ticker.unique() if i != pred_ticker]
    dfml = full_df[full_df.ticker == pred_ticker].drop('ticker', axis=1)
    dfml.rename({'percent_change_feat': f'{pred_ticker}_percent_change_{feat_days}'}, axis=1, inplace=True)
    dfml.rename({'percent_change_pred': f'{pred_ticker}_percent_change_pred'}, axis=1, inplace=True)
    for ticker in feature_tickers:
        help_df = full_df[full_df.ticker == ticker][['past_date', 'current_date', 'prediction_date', 'percent_change_feat']]
        help_df.rename({'percent_change_feat': f'{ticker}_percent_change_{feat_days}'}, axis=1, inplace=True)
        dfml = pd.merge(dfml, help_df,
                        left_on=['past_date', 'current_date', 'prediction_date'],
                        right_on=['past_date', 'current_date', 'prediction_date'],
                        how='left')
    return dfml


def generate_testing_matrix(full_df, feat_days):
    """generates a testing matrix with features based on all tickers

    Args:
        full_df (df): all features
        feat_days (int): number of feature days in change

    Returns:
        df: machine learning dataframe with dates
    """
    pred_ticker = full_df.ticker.unique()[0]
    feature_tickers = [i for i in full_df.ticker.unique() if i != pred_ticker]
    dfml = full_df[full_df.ticker == pred_ticker].drop('ticker', axis=1)
    dfml.rename({'percent_change_feat': f'{pred_ticker}_percent_change_{feat_days}'}, axis=1, inplace=True)
    for ticker in feature_tickers:
        help_df = full_df[full_df.ticker == ticker][['past_date', 'current_date', 'prediction_date', 'percent_change_feat']]
        help_df.rename({'percent_change_feat': f'{ticker}_percent_change_{feat_days}'}, axis=1, inplace=True)
        dfml = pd.merge(dfml, help_df,
                        left_on=['past_date', 'current_date', 'prediction_date'],
                        right_on=['past_date', 'current_date', 'prediction_date'],
                        how='left')
    return dfml.drop('percent_change_pred', axis=1)


def generate_daily_matrix(full_df, feat_days):
    """generates a testing matrix with features based on all tickers

    Args:
        full_df (df): all features
        feat_days (int): number of feature days in change

    Returns:
        df: machine learning dataframe with dates
    """
    pred_ticker = full_df.ticker.unique()[0]
    feature_tickers = [i for i in full_df.ticker.unique() if i != pred_ticker]
    dfml = full_df[full_df.ticker == pred_ticker].drop('ticker', axis=1)
    dfml.rename({'percent_change_pred': f'{pred_ticker}_percent_change_{feat_days}'}, axis=1, inplace=True)
    for ticker in feature_tickers:
        help_df = full_df[full_df.ticker == ticker][['past_date', 'current_date', 'prediction_date', 'percent_change_pred']]
        help_df.rename({'percent_change_pred': f'{ticker}_percent_change_{feat_days}'}, axis=1, inplace=True)
        dfml = pd.merge(dfml, help_df,
                        left_on=['past_date', 'current_date', 'prediction_date'],
                        right_on=['past_date', 'current_date', 'prediction_date'],
                        how='left')
    return dfml.drop('percent_change_feat', axis=1)

# def create_feats(price_df, feat_days):
#     """creates a feature and dataframe for machine learning

#     Args:
#         price_df (df): pricing information with ticker, date, and price
#         feat_days (int): number of feature days

#     Returns:
#         df: ml features dataframe
#     """

#     # create shifted percent features
#     df_feats = price_n_days_out(price_df, days=feat_days)
#     df_help = df_feats.copy()[['ticker', 'prediction_date', f'price_{feat_days}_out']]
#     df_help.columns = ['ticker', 'date', 'close']

#     # do some cleaning
#     full_df = pd.merge(df_feats, df_preds, left_on=['ticker', 'prediction_date'], right_on=['ticker', 'date'])
#     full_df.columns = ['ticker', 'past_date', 'past_close', 'current_date', 'current_price',
#                        'percent_change_feat', 'date_y', 'close_y', 'prediction_date',
#                        'price_5_out_y', 'percent_change_pred']
#     full_df = full_df[['ticker', 'past_date', 'current_date', 'prediction_date',
#                        'percent_change_feat', 'percent_change_pred']]
#     return full_df
