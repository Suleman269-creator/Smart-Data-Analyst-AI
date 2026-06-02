import pandas as pd
import numpy as np

def clean_dataset(df):
    if df is None or df.empty:
        return df

    df_clean = df.copy()

    # 1. FORCE DROP: Instantly drops any trailing unnamed ghost columns
    unnamed_cols = [c for c in df_clean.columns if 'unnamed' in str(c).lower() or str(c).strip() == '']
    if unnamed_cols:
        df_clean = df_clean.drop(columns=unnamed_cols)

    # 2. Standardize all column header names (Lowercase & Snake Case)
    df_clean.columns = df_clean.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')

    # 3. Dynamic Numeric Cleaning for Financial Metrics
    target_numeric_cols = [c for c in df_clean.columns if any(k in c for k in ['revenue', 'profit', 'cost', 'sales', 'discount', 'quantity'])]

    for col in target_numeric_cols:
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].str.replace('Rs', '', regex=False)\
                                         .str.replace('Rs.', '', regex=False)\
                                         .str.replace('$', '', regex=False)\
                                         .str.replace(',', '', regex=False)
            df_clean[col] = df_clean[col].replace(['None', 'nan', 'Null', 'null', ''], np.nan)
        
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0.0)

    # 4. Clean Category/Product Strings
    cat_col = next((c for c in df_clean.columns if 'category' in c or 'product' in c), None)
    if cat_col:
        df_clean[cat_col] = df_clean[cat_col].astype(str).str.strip().str.title()
        df_clean = df_clean[~df_clean[cat_col].isin(['Nan', 'None', '', 'Null'])]

    # 5. Standardize Order Dates
    date_col = next((c for c in df_clean.columns if 'date' in c or 'time' in c), None)
    if date_col:
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')

    return df_clean