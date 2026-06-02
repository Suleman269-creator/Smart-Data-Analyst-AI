import streamlit as st
from groq import Groq
import pandas as pd
import re

def aggressive_clean_numeric(series):
    """Safely cast formatted currency text into raw calculation metrics"""
    if series is None:
        return 0.0
    s = series.astype(str).str.strip().str.lower()
    s = s.str.replace('$', '', regex=False).str.replace('rs', '', regex=False)\
             .str.replace('rs.', '', regex=False).str.replace(',', '', regex=False)
    s = s.replace(['none', 'nan', 'null', ''], '0')
    s = s.apply(lambda x: re.sub(r'[^0-9.-]', '', x) if isinstance(x, str) else x)
    s = s.replace(['', '-'], '0')
    return pd.to_numeric(s, errors='coerce').fillna(0.0)

def get_insights(df):
    if df is None or df.empty:
        return "No data profile matches available."
        
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return "❌ Configuration Error: 'GROQ_API_KEY' not found in .streamlit/secrets.toml."

    client = Groq(api_key=api_key)
    df_ai = df.copy()

    # Pre-clean the metric arrays to calculate true parameters natively
    cols = df_ai.columns.tolist()
    rev_col = next((c for c in cols if 'revenue' in c.lower() or 'sales' in c.lower()), None)
    prof_col = next((c for c in cols if 'profit' in c.lower()), None)
    cost_col = next((c for c in cols if 'cost' in c.lower()), None)

    if rev_col: df_ai[rev_col] = aggressive_clean_numeric(df_ai[rev_col])
    if prof_col: df_ai[prof_col] = aggressive_clean_numeric(df_ai[prof_col])
    if cost_col: df_ai[cost_col] = aggressive_clean_numeric(df_ai[cost_col])

    # Pre-calculate pure high-fidelity numbers natively in Python
    total_orders = len(df_ai)
    total_rev = df_ai[rev_col].sum() if rev_col else 0.0
    total_prof = df_ai[prof_col].sum() if prof_col else 0.0
    total_cost = df_ai[cost_col].sum() if cost_col else 0.0
    
    avg_order_value = total_rev / total_orders if total_orders > 0 else 0.0
    profit_margin_pct = (total_prof / total_rev) * 100 if total_rev > 0 else 0.0

    # STRICT INSTRUCTION PROMPT: Forbids LaTeX notation entirely
    prompt = f"""
    You are an expert Executive Corporate BI Consultant. Analyze these exact, live data metrics:
    - Total Rows Processed: {total_orders:,}
    - Cumulative Gross Revenue: ${total_rev:,.0f}
    - Total Operational Cost: ${total_cost:,.0f}
    - Net Profit Realized: ${total_prof:,.0f}
    - Average Revenue Per Transaction: ${avg_order_value:,.0f}
    - Net Profit Margin Ratio: {profit_margin_pct:.1f}%

    Provide exactly 3 key actionable trend observations and strategic recommendations.
    
    STRICT FORMATTING RULES:
    1. Do NOT use dollar signs inside math symbols. Write currency values as standard text strings (e.g., $100,000 or $41,368,854).
    2. Do NOT use markdown math blocks, LaTeX brackets, or text wrapping tags like '$' or '$$' anywhere in your response. 
    3. Ensure all text sentences utilize standard spacing. Write purely in clean, executive business English prose.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, # Low temperature ensures strict alignment to rules
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Groq AI Cloud Gateway Error: {str(e)}"