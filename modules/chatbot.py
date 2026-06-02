import streamlit as st
from groq import Groq
import pandas as pd

def chat_with_data(df, question):
    if df is None or df.empty:
        return "No data records accessible."

    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return "❌ Configuration Error: 'GROQ_API_KEY' not found in .streamlit/secrets.toml."

    client = Groq(api_key=api_key)

    # 1. DYNAMIC CONTEXT GENERATION: Build summaries of the ENTIRE dataset (all 20+ rows)
    num_rows, num_cols = df.shape
    
    # Isolate targets dynamically based on your clean headers
    cat_col = next((c for c in df.columns if 'category' in c or 'product' in c), None)
    
    # Calculate a full group summary matrix so the AI knows the exact math totals
    if cat_col:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        summary_matrix = df.groupby(cat_col)[numeric_cols].sum().to_string()
    else:
        summary_matrix = df.select_dtypes(include='number').sum().to_string()

    # 2. Package everything into a tight system context prompt
    prompt = f"""
    You are an expert corporate AI Data Analyst assistant. You are analyzing a dataset with {num_rows} total transactions.
    
    Here is the exact mathematical sum total matrix computed across the ENTIRE dataset:
    {summary_matrix}
    
    User Query: "{question}"
    
    Instructions:
    Answer the user's question directly and concisely using the exact totals from the calculation matrix provided above. If asked for a specific total, extract it from the matrix. Do not say you are only looking at 5 rows.
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2 # Lower temperature prevents the model from hallucinating numbers
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Groq Connection Fault: {str(e)}"