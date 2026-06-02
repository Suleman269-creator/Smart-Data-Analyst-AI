import pandas as pd

def generate_kpis(df):
    kpis = {
        'total_revenue': 0,
        'total_cost': 0,
        'total_profit': 0,
        'total_rows': 0
    }
    
    if df is None or df.empty:
        return kpis

    cols = df.columns.tolist()
    rev_col = next((c for c in cols if 'revenue' in c or 'sales' in c), None)
    cost_col = next((c for c in cols if 'cost' in c), None)
    prof_col = next((c for c in cols if 'profit' in c), None)

    # Compute explicit sum configurations across variables
    if rev_col:
        kpis['total_revenue'] = int(df[rev_col].sum())
    if cost_col:
        kpis['total_cost'] = int(df[cost_col].sum())
    if prof_col:
        kpis['total_profit'] = int(df[prof_col].sum())
        
    kpis['total_rows'] = len(df)
    return kpis