import pandas as pd
import numpy as np
import re

def clean_dataset(df):
    """
    Executes an aggressive data cleansing pipeline. Normalizes headers, handles
    unaligned datetime sequences, eliminates categorical 'None' ambiguity, and 
    forces mixed string/numeric data blocks into clean float vectors.
    """
    if df is None or df.empty:
        return df

    # Create an isolated deep copy to prevent mutating underlying memory spaces
    df_clean = df.copy()

    # 1. FORCE DROP: Instantly remove trailing unnamed ghost delimiter tracks
    unnamed_cols = [c for c in df_clean.columns if 'unnamed' in str(c).lower() or str(c).strip() == '']
    if unnamed_cols:
        df_clean = df_clean.drop(columns=unnamed_cols)

    # 2. STANDARDIZE HEADERS: Convert to lowercase, trimmed, snake_case format layout
    df_clean.columns = df_clean.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')

    # 3. FIXED CATEGORICAL CLEANING: Replace ambiguous 'None/Null' strings with a clean label
    cat_col = next((c for c in df_clean.columns if 'category' in c or 'product' in c), None)
    if cat_col:
        # Force column data types to string and strip flanking blank spaces
        df_clean[cat_col] = df_clean[cat_col].astype(str).str.strip()
        
        # Create a boolean filter mask to identify variations of empty or missing fields
        null_mask = df_clean[cat_col].str.lower().isin(['nan', 'none', '', 'null', 'default'])
        
        # Safely impute those specific positions with a professional fallback category name
        df_clean.loc[null_mask, cat_col] = "Uncategorized"
        
        # Apply standard Title Casing format (e.g., "Home Appliances", "Uncategorized")
        df_clean[cat_col] = df_clean[cat_col].str.title()

    # 4. DATETIME ALIGNMENT: Standardize and align timeline attributes safely
    date_col = next((c for c in df_clean.columns if 'date' in c or 'time' in c), None)
    if date_col:
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')

    # 5. FIXED REGEX PARSER: Processes mixed string formats and raw integers smoothly
    for col in df_clean.columns:
        # Evaluate target operational financial metrics columns
        if any(keyword in str(col).lower() for keyword in ['revenue', 'profit', 'cost', 'sales', 'amount']):
            
            # Step A: Force every single cell in the series to a clean string layout first
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