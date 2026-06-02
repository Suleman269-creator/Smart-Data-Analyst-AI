import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from groq import Groq

def run_prediction(df, x_col, y_col):
    if df is None or df.empty:
        st.error("No active dataset available for training.")
        return

    # 1. Isolate target columns and clean numeric data types natively
    df_clean = df[[x_col, y_col]].copy()
    df_clean[x_col] = pd.to_numeric(df_clean[x_col], errors='coerce')
    df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce')
    df_clean = df_clean.dropna()
    
    if df_clean.empty:
        st.error("❌ Data error: No valid numeric data rows remaining for model training.")
        return

    # 2. Extract raw matrix arrays for Scikit-Learn training execution
    X = df_clean[[x_col]].values
    y = df_clean[y_col].values

    # 3. Train the Linear Regression Model natively
    model = LinearRegression()
    model.fit(X, y)
    
    # Extract structural math parameters
    r2_score = model.score(X, y)
    slope = model.coef_[0]
    intercept = model.intercept_

    # 4. Render Metric Summary Display Cards
    st.markdown("#### 📊 Core Mathematical Indicators")
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric("Model Explanatory R² Score Index", f"{r2_score:.4f}")
    with m_col2:
        st.metric("Calculated Line Slope (Beta Coefficient)", f"{slope:.4f}")

    # 5. STREAM CONTEXT TO GROQ FOR AUTO-EXPLANATION
    st.markdown("#### 🤖 Automated Executive Regression Narrative")
    
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.warning("⚠️ 'GROQ_API_KEY' not found. Cannot generate narrative explanation.")
        return

    client = Groq(api_key=api_key)

    # Build the analytical framing prompt for Groq
    prompt = f"""
    You are an elite business analyst. A user has trained a Linear Regression machine learning model on their sales data.
    
    Here are the exact output metrics from scikit-learn:
    - Independent Predictor (X): {x_col.replace('_', ' ').title()}
    - Dependent Target (Y): {y_col.replace('_', ' ').title()}
    - R-Squared Accuracy Score: {r2_score:.4f} (or {r2_score*100:.2f}%)
    - Line Slope (Beta Coefficient): {slope:.4f}
    - Y-Intercept Constant: {intercept:.4f}
    
    Instructions:
    Write a clear, professional, and easy-to-read explanation of these results for a non-technical manager or professor.
    1. Break down what the R-squared score means in plain English regarding prediction reliability.
    2. Explain exactly what the Slope means (e.g., 'For every 1 unit increase in X, Y goes up/down by...').
    3. Keep it to 3 concise, bulleted business observations with clear spacing. Do not show raw formulas or code blocks.
    """

    with st.spinner("Groq AI is analyzing the regression matrices..."):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            # Render the AI explanation inside a clean callout box container
            st.info(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Groq narrative compilation faulted: {str(e)}")