import pandas as pd
import numpy as np
import re

def clean_dataset(df):
    if df is None or df.empty:
        return df

    df_clean = df.copy()

    # 1. FORCE DROP: Instantly remove trailing unnamed ghost delimiter tracks
    unnamed_cols = [c for c in df_clean.columns if 'unnamed' in str(c).lower() or str(c).strip() == '']
    if unnamed_cols:
        df_clean = df_clean.drop(columns=unnamed_cols)

    # 2. Standardize Column Headers (Lowercase, Trimmed, Snake Case Layout)
    df_clean.columns = df_clean.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')

    # 3. Clean Category / Product String Structural Attributes
    cat_col = next((c for c in df_clean.columns if 'category' in c or 'product' in c), None)
    if cat_col:
        df_clean[cat_col] = df_clean[cat_col].astype(str).str.strip().str.title()
        df_clean = df_clean[~df_clean[cat_col].isin(['Nan', 'None', '', 'Null'])]

    # 4. Standardize and Align Order Timeline Datetime Attributes
    date_col = next((c for c in df_clean.columns if 'date' in c or 'time' in c), None)
    if date_col:
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')

    # 5. FIXED: Aggressive mixed-type numeric column cleaner loop
    for col in df_clean.columns:
        if any(k in str(col).lower() for k in ['revenue', 'profit', 'cost', 'sales', 'amount']):
            # Step A: Force every single cell in the series to a clean string format first
            s = df_clean[col].astype(str).str.strip().str.lower()
            
            # Step B: Strip out dollar signs, commas, and currency labels safely
            s = s.str.replace('$', '', regex=False)
            s = s.str.replace('rs', '', regex=False)
            s = s.str.replace('rs.', '', regex=False)
            s = s.str.replace(',', '', regex=False)
            
            # Step C: Replace text-based null values with literal '0' text
            s = s.replace(['none', 'nan', 'null', ''], '0')
            
            # Step D: Use regex to strip any remaining non-numeric text characters
            s = s.apply(lambda x: re.sub(r'[^0-9.-]', '', x) if isinstance(x, str) else x)
            s = s.replace(['', '-'], '0')
            
            # Step E: Cast to numeric float, filling any parsing errors with 0.0
            df_clean[col] = pd.to_numeric(s, errors='coerce').fillna(0.0)

    return df_clean