import pickle
import datetime as dt
import pandas as pd
import numpy as np
import os

from . import scrape
from . import preprocess
from . import ml

from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class TabularML():

    def __init__(self, ticker, today, file_path):
        self.ticker = ticker
        self.today = dt.datetime.strptime(today, '%Y-%m-%d').date()
        self.file_path = f'{file_path}/{ticker}/'

    def load_ml_files(self):
        with open(f'{self.file_path}predictor.pickle', 'rb') as f:
            self.predictor = pickle.load(f)
        with open(f'{self.file_path}scalerML.pickle', 'rb') as f:
            self.scalerML = pickle.load(f)
        with open(f'{self.file_path}scalerReal.pickle', 'rb') as f:
            self.scalerReal = pickle.load(f)
        with open(f'{self.file_path}PCA.pickle', 'rb') as f:
            self.PCA = pickle.load(f)
        with open(f'{self.file_path}model_specifiers.pickle', 'rb') as f:
            self.model_specifiers = pickle.load(f)

    def scrape_prices(self, file_override=None):
        if file_override is not None:
            pass
        else:
            start = self.today - dt.timedelta(days=self.model_specifiers['feat_days']+7)
            stop = self.today
            self.price_df = scrape.get_prices(self.model_specifiers['tickers'],
                                              start,
                                              stop,
                                              price_types=['Close'],)

    def generate_feature_vector(self):
        df_feats = preprocess.price_n_days_out(self.price_df, days=self.model_specifiers['feat_days'])
        df_feats = df_feats[df_feats.prediction_date == str(self.today)]
        feat_days = self.model_specifiers['feat_days']
        df_feats = df_feats[['ticker', 'prediction_date', f'percent_{feat_days}_out']]
        df_feats.columns = ['ticker', 'prediction_date', f'percent_change_{feat_days}']
        pred_ticker = self.ticker
        feature_tickers = [i for i in df_feats.ticker.unique() if i != pred_ticker]
        self.dfml = df_feats[df_feats.ticker == pred_ticker].drop('ticker', axis=1)
        self.dfml.rename({f'percent_change_{feat_days}': f'{pred_ticker}_percent_change_{feat_days}'}, axis=1, inplace=True)
        for ticker in feature_tickers:
            help_df = df_feats[df_feats.ticker == ticker][['prediction_date', f'percent_change_{feat_days}']]
            help_df.rename({f'percent_change_{feat_days}': f'{ticker}_percent_change_{feat_days}'}, axis=1, inplace=True)
            self.dfml = pd.merge(self.dfml, help_df,
                                 left_on=['prediction_date'],
                                 right_on=['prediction_date'],
                                 how='left')
        self.dfml = self.dfml.drop('prediction_date', axis=1)

    def full_predict(self):
        pc_vec = self.PCA.transform(self.dfml)
        raw_pred = self.predictor.predict(pc_vec)
        z_pred = self.scalerML.transform([raw_pred])
        y = self.scalerReal.inverse_transform(z_pred)
        return y


class ModelTrain():
    def __init__(self, ticker, price_df, file_path, feat_days=5, pred_days=5):
        self.pred_ticker = ticker
        self.price_df = price_df
        self.feat_days = feat_days
        self.pred_days = pred_days
        self.file_path = file_path

    def preprocess_data(self):
        full_df = preprocess.create_feats_and_preds(self.price_df, self.feat_days, self.pred_days)
        self.dfml = preprocess.generate_ml_matrix(full_df, self.pred_ticker, self.feat_days)
        self.dfml = self.dfml.fillna(0)
        self.y_var = f'{self.pred_ticker}_percent_change_pred'
        self.feat_cols = [i for i in self.dfml.columns if 'date' not in i and i != self.y_var]

    def reduce_dimensions(self):
        self.pca = PCA(n_components=10)
        self.X = self.pca.fit_transform(self.dfml[self.feat_cols])
        self.y = self.dfml[[self.y_var]].to_numpy()

    def hypertune(self):
        self.train_X, self.test_X, self.train_y, self.test_y = train_test_split(self.X, self.y, test_size=0.25, random_state=42)
        self.train_y, self.test_y = np.ravel(self.train_y), np.ravel(self.test_y)
        params = {
            'n_estimators': [50, 100, 150, 200, 300, 500],
            'max_depth': range(2, 10),
            'min_samples_split': range(5, 100),
        }
        model = RandomForestRegressor(n_estimators=100, random_state=42, oob_score=True)
        n_iters = 100
        clf = RandomizedSearchCV(model, params, random_state=42, verbose=0, n_iter=n_iters, n_jobs=-1)
        search = clf.fit(self.train_X, self.train_y)
        self.hypertune_params = search.best_params_

    def generate_model(self):
        self.rf = RandomForestRegressor(**self.hypertune_params, oob_score=True, random_state=42)
        self.rf.fit(self.train_X, self.train_y)
        pred_train_labels = self.rf.predict(self.train_X)
        pred_test_labels = self.rf.predict(self.test_X)

        self.scalerML = StandardScaler()
        self.scalerML.fit(pred_train_labels.reshape(-1, 1))
        self.scalerReal = StandardScaler()
        self.scalerReal.fit(self.train_y.reshape(-1, 1))
        y_pred_z = self.scalerML.transform(pred_test_labels.reshape(-1, 1)).T[0]
        y_pred_real = self.scalerReal.inverse_transform(y_pred_z.reshape(-1, 1)).T[0]

        res = pd.DataFrame()
        res['actual'] = self.test_y
        res['prediction'] = y_pred_real
        ml.result_report(res, threshold=0.01, verbose=True)

    def save_model_files(self):
        model_specifiers = {
            'tickers': [i.replace(f'_percent_change_{self.feat_days}', '') for i in self.feat_cols],
            'feat_days': 5,
            'pred_days': 5,
        }
        if not os.path.exists(f'{self.file_path}/{self.pred_ticker}'):
            os.makedirs(f'{self.file_path}/{self.pred_ticker}')
        with open(f'{self.file_path}/{self.pred_ticker}/predictor.pickle', 'wb') as f:
            pickle.dump(self.rf, f)
        with open(f'{self.file_path}/{self.pred_ticker}/scalerML.pickle', 'wb') as f:
            pickle.dump(self.scalerML, f)
        with open(f'{self.file_path}/{self.pred_ticker}/scalerReal.pickle', 'wb') as f:
            pickle.dump(self.scalerReal, f)
        with open(f'{self.file_path}/{self.pred_ticker}/PCA.pickle', 'wb') as f:
            pickle.dump(self.pca, f)
        with open(f'{self.file_path}/{self.pred_ticker}/model_specifiers.pickle', 'wb') as f:
            pickle.dump(model_specifiers, f)
