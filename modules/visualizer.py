import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def clean_numeric_directly(series):
    """Aggressively strip currency symbols, commas, spaces, and force clean floats"""
    if series is None:
        return 0.0
    # Convert to string, strip whitespace, remove common punctuation
    s_clean = series.astype(str).str.strip()
    s_clean = s_clean.str.replace('$', '', regex=False)
    s_clean = s_clean.str.replace('Rs', '', regex=False)
    s_clean = s_clean.str.replace('Rs.', '', regex=False)
    s_clean = s_clean.str.replace(',', '', regex=False)
    
    # Handle explicit text nulls
    s_clean = s_clean.replace(['None', 'nan', 'NaN', 'Null', 'null', ''], '0')
    
    # Force convert to numeric, replace errors with 0
    return pd.to_numeric(s_clean, errors='coerce').fillna(0.0)

def show_dashboard(df):
    if df is None or df.empty:
        st.error("Visualizer received an empty dataset.")
        return

    # Isolate a clean local copy
    df_chart = df.copy()

    # Dynamic Column Identifier Map
    cols = df_chart.columns.tolist()
    cat_col = next((c for c in cols if 'category' in c.lower() or 'product' in c.lower()), None)
    rev_col = next((c for c in cols if 'revenue' in c.lower() or 'sales' in c.lower()), None)
    prof_col = next((c for c in cols if 'profit' in c.lower()), None)
    date_col = next((c for c in cols if 'date' in c.lower() or 'time' in c.lower()), None)

    # Force strict conversion on the visualization layer
    if rev_col:
        df_chart[rev_col] = clean_numeric_directly(df_chart[rev_col])
    if prof_col:
        df_chart[prof_col] = clean_numeric_directly(df_chart[prof_col])

    if cat_col:
        df_chart[cat_col] = df_chart[cat_col].astype(str).str.strip().str.title()
        df_chart = df_chart[~df_chart[cat_col].isin(['Nan', 'None', '', 'Null'])]

    st.subheader("📈 Customer Performance Visual Analytics")
    col1, col2 = st.columns(2)

    # ============================
    # 1. FIXED VERTICAL BAR CHART
    # ============================
    with col1:
        if cat_col and rev_col and prof_col:
            st.markdown("#### 🏢 Total Revenue & Profit by Category")
            
            # Aggregate true floating-point mathematical sums
            summary_df = df_chart.groupby(cat_col, as_index=False)[[rev_col, prof_col]].sum()

            fig1 = go.Figure()
            
            # Revenue Bars
            fig1.add_trace(go.Bar(
                x=summary_df[cat_col], 
                y=summary_df[rev_col], 
                name="Total Revenue",
                marker_color='#8b5cf6', 
                text=summary_df[rev_col].apply(lambda x: f"${x:,.0f}"),
                textposition='outside'
            ))
            
            # Profit Bars
            fig1.add_trace(go.Bar(
                x=summary_df[cat_col], 
                y=summary_df[prof_col], 
                name="Net Profit",
                marker_color='#ec4899', 
                text=summary_df[prof_col].apply(lambda x: f"${x:,.0f}"),
                textposition='outside'
            ))

            fig1.update_layout(
                template='plotly_dark', 
                barmode='group', 
                height=400,
                xaxis_title="Product Category", 
                yaxis_title="Financial Value ($)",
                yaxis=dict(tickformat="$,.0f"), # Dynamically scale axis into thousands/millions
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig1, use_container_width=True)

    # ============================
    # 2. FIXED REVENUE TREE-MAP
    # ============================
    with col2:
        if cat_col and rev_col:
            st.markdown("#### 📦 Category Market Volume Share")

            treemap_df = df_chart.groupby(cat_col, as_index=False)[rev_col].sum()

            # Fix syntax error by building custom explicit layout hover text labels
            labels = treemap_df[cat_col].tolist()
            values = treemap_df[rev_col].tolist()
            total_val = sum(values) if sum(values) > 0 else 1
            
            # Pre-calculate text tags manually to avoid browser string template glitches
            text_tags = [f"{l}<br>${v:,.0f}<br>({(v/total_val)*100:.1f}%)" for l, v in zip(labels, values)]

            fig2 = go.Figure(go.Treemap(
                labels=labels,
                parents=[""] * len(labels),
                values=values,
                text=text_tags,
                textinfo="text",
                marker=dict(colors=values, colorscale='Purples')
            ))

            fig2.update_layout(
                template='plotly_dark', 
                height=400,
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ============================
    # 3. CHRONOLOGICAL TIMELINE
    # ============================
    if date_col and rev_col and prof_col:
        st.markdown("#### 📅 Financial Growth Timeline")
        df_chart[date_col] = pd.to_datetime(df_chart[date_col], errors='coerce')
        df_sorted = df_chart.dropna(subset=[date_col]).sort_values(date_col)

        time_df = df_sorted.groupby(df_sorted[date_col].dt.to_period("M"))[[rev_col, prof_col]].sum().reset_index()
        time_df[date_col] = time_df[date_col].astype(str)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=time_df[date_col], y=time_df[rev_col], mode='lines+markers', name='Revenue', line=dict(width=3, color='#a855f7')))
        fig3.add_trace(go.Scatter(x=time_df[date_col], y=time_df[prof_col], mode='lines+markers', name='Profit', line=dict(width=2, dash='dash', color='#ec4899')))

        fig3.update_layout(
            template='plotly_dark', height=400, title="Monthly Performance Trend",
            xaxis_title="Chronological Order Timeline", yaxis_title="Financial Scale ($)",
            yaxis=dict(tickformat="$,.0f"), xaxis=dict(type='category')
        )
        st.plotly_chart(fig3, use_container_width=True)