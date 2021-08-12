# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_dstools_preparedata.ipynb (unless otherwise specified).

__all__ = ['EncodeCats', 'FixMissing', 'Normalize', 'numericalize', 'split_data']

# Cell
from ..imports import *

# Cell
class EncodeCats:
    """
    How to Use:
    encode = EncodeCats()
    fixmissing = FixMissing()
    normalize = Normalize()
    df, categories = encode.apply_train(df, cat_vars)
    df, na_dict = fixmissing.apply_train(df, cont_vars, cat_vars, add_col=True)
    df, means, stds = normalize.apply_train(df, cont_vars)
    """

    def __init__(self):
        self.categories = {}

    def apply_train(self, df, cat_vars):
        """Transform cat_vars columns in categoricals"""
        for n in cat_vars:
            df.loc[:, n] = df.loc[:, n].astype('category').cat.as_ordered()
            self.categories[n] = df[n].cat.categories
        return df, self.categories

    @staticmethod
    def apply_test(df, cat_vars, categories):
        """Apply transform of cat_vars from training to test"""
        for n in cat_vars:
            df.loc[:, n] = pd.Categorical(df[n], categories=categories[n], ordered=True)   # noqa:

# Cell
class FixMissing:

    @staticmethod
    def apply_train(df, cont_vars, cat_vars, add_col=True):
        """Fill missing in cont_vars"""
        na_dict = {}
        for name in cont_vars:
            if pd.isnull(df[name]).sum():
                if add_col:
                    df[name + '_na'] = pd.isnull(df[name])
                filler = df[name].median()
                df[name] = df[name].fillna(filler)
                na_dict[name] = filler
        return df, na_dict

    @staticmethod
    def apply_test(df, cont_vars, cat_vars, na_dict, add_col=True):
        """Fill missing values in cont_vars like apply train"""
        for name in cont_vars:
            if name in na_dict:
                if add_col:
                    df[name + '_na'] = pd.isnull(df[name])
                df[name] = df[name].fillna(na_dict[name])
            elif pd.isnull(df[name]).sum() != 0:
                raise Exception(f"""There are nan values in field {name}.""")

# Cell
class Normalize:

    @staticmethod
    def apply_train(df, cont_vars):
        """Computer the means and stds of cont_name columns to normalize them"""   # noqa:
        means, stds = {}, {}
        for n in cont_vars:
            assert is_numeric_dtype(df[n]), f"""Can't normalize '{n}' column as it isn't numerical."""  # noqa:
            means[n], stds[n] = df[n].mean(), df[n].std()
            df[n] = (df[n] - means[n]) / (1e-7 + stds[n])
        return df, means, stds

    @staticmethod
    def apply_test(df, means, stds, cont_vars):
        """Normalize cont_vars with the same statistics in apply_train"""
        for n in cont_vars:
            df[n] = (df[n] - means[n]) / (1e-7 + stds[n])

# Cell
def numericalize(df, col, name, max_n_cat):
    """Numericalize is used to encode the categorical variables for model use"""   # noqa:
    if not is_numeric_dtype(col) and (max_n_cat is None or len(col.cat.categories) > max_n_cat):  # noqa:
        df[name] = col.cat.codes + 1

# Cell
def split_data(df, y_fld=None, max_n_cat=None):
    """split_data is the last step in preparing a data set for model ingestion"""   # noqa:
    df = df.copy()
    if y_fld is None:
        y = None
    else:
        if not is_numeric_dtype(df[y_fld]):
            df[y_fld] = df[y_fld].cat.codes
        y = df[y_fld].values
    df.drop(y_fld, axis=1, inplace=True)
    for n, c in df.items():
        numericalize(df, c, n, max_n_cat)
    return df, y