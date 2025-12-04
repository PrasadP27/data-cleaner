# cleaning_model.py
import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import re

def load_data_from_filelike(file_obj, filename: str) -> pd.DataFrame:
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(file_obj)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_obj)
    else:
        raise ValueError(f"Unsupported format: {ext}")
    return df

def remove_blank_columns(df):
    """Stage 2: Drop columns that are 100% empty."""
    if df is None: return None
    df_cleaned = df.dropna(axis=1, how='all')
    return df_cleaned

def remove_blank_rows(df):
    """Stage 3: Drop rows that are 100% empty."""
    if df is None: return None
    df_cleaned = df.dropna(axis=0, how='all')
    return df_cleaned

def clean_gibberish(df):
    """Stage 4: Identify and remove 'junk' strings."""
    if df is None: return None
    obj_cols = df.select_dtypes(include=['object']).columns
    gibberish_pattern = r'^[^a-zA-Z0-9]+$'

    for col in obj_cols:
        series = df[col].astype(str)
        garbage_mask = series.str.strip().str.match(gibberish_pattern) | \
                       (series.str.strip() == '') | \
                       (series == 'nan')
        
        if garbage_mask.any():
            df.loc[garbage_mask, col] = np.nan
    return df

def impute_categorical(df, fill_value="NaN"):
    """Stage 5: Fill NaN in string columns."""
    if df is None: return None
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        df[cat_cols] = df[cat_cols].fillna(fill_value)
    return df

def impute_numeric_knn(df, n_neighbors=5):
    """Stage 6: Fill NaN in numeric columns using KNN."""
    if df is None: return None
    num_cols = df.select_dtypes(include=['number']).columns
    if len(num_cols) > 0:
        imputer = KNNImputer(n_neighbors=n_neighbors)
        df[num_cols] = pd.DataFrame(imputer.fit_transform(df[num_cols]), 
                                    columns=num_cols, 
                                    index=df.index)
    return df

def run_cleaning_pipeline( df: pd.DataFrame,
    *,
    drop_columns: bool = True,
    drop_rows: bool = True,
    clean_strings: bool = True,
    impute_cats: bool = True,
    impute_nums: bool = True,
    fill_value: str = "NaN",
    n_neighbors: int = 5,) -> pd.DataFrame:
    """Run only the steps selected by the user."""
    if drop_columns:
        df = remove_blank_columns(df)
    if drop_rows:
        df = remove_blank_rows(df)
    if clean_strings:
        df = clean_gibberish(df)
    if impute_cats:
        df = impute_categorical(df, fill_value=fill_value)
    if impute_nums:
        df = impute_numeric_knn(df, n_neighbors=n_neighbors)
    return df
