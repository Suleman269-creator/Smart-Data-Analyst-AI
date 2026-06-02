import streamlit as st
from modules.loader import load_file
from modules.cleaner import clean_dataset
from modules.analyzer import generate_kpis
from modules.visualizer import show_dashboard
from modules.ai_engine import get_insights
from modules.chatbot import chat_with_data
from modules.predictor import run_prediction

# 1. Page Configuration
st.set_page_config(
    page_title="Customer AI Data Analyst", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Advanced Premium CSS: Custom Dark Mode, Purple Gradients & Glowing Cards
st.markdown("""
    <style>
        /* Global Background & Font Tuning */
        .stApp {
            background-color: #0d0b14;
            color: #f1f0f5;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
        
        /* Centralized Hero Title Styling */
        .hero-container {
            text-align: center;
            padding: 2.5rem 1rem 1.5rem 1rem;
            background: linear-gradient(135deg, rgba(31,18,54,0.6) 0%, rgba(15,10,28,0.6) 100%);
            border-radius: 16px;
            border: 1px solid rgba(147, 51, 234, 0.2);
            margin-bottom: 2.5rem;
            box-shadow: 0 8px 32px 0 rgba(147, 51, 234, 0.05);
        }
        .hero-title {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(90deg, #d8b4fe 0%, #a855f7 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
            letter-spacing: -0.5px;
        }
        .hero-caption {
            font-size: 16px;
            color: #94a3b8;
            margin-top: 8px;
            font-weight: 400;
        }

        /* Modern Dashboard Section Subheaders */
        .section-header {
            font-size: 22px;
            font-weight: 700;
            color: #e2e8f0;
            border-left: 4px solid #a855f7;
            padding-left: 12px;
            margin-top: 2rem;
            margin-bottom: 1.2rem;
            letter-spacing: -0.3px;
        }

        /* Premium Glassmorphic Cards for KPIs */
        div[data-testid="stMetric"] {
            background: rgba(25, 18, 41, 0.45) !important;
            border: 1px solid rgba(168, 85, 247, 0.2) !important;
            border-radius: 12px !important;
            padding: 1.25rem !important;
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2) !important;
            transition: all 0.3s ease-in-out !important;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(236, 72, 153, 0.4) !important;
            box-shadow: 0 8px 25px 0 rgba(168, 85, 247, 0.1) !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px !important;
            font-weight: 800 !important;
            background: linear-gradient(90deg, #c084fc, #f472b6) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 12px !important;
            font-weight: 600 !important;
            color: #94a3b8 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.75px !important;
        }

        /* Premium Gradient Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 100%) !important;
            color: #ffffff !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2) !important;
        }
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4) !important;
            opacity: 0.95;
        }
        .stButton>button:active {
            transform: translateY(1px) !important;
        }

        /* Form & Input Container Customization */
        div[data-testid="stForm"] {
            background: rgba(18, 14, 30, 0.7) !important;
            border: 1px solid rgba(168, 85, 247, 0.15) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
        }

        /* Clean Separators */
        hr {
            border-color: rgba(168, 85, 247, 0.1) !important;
            margin: 2.5rem 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Centralized Hero Title Section (FIXED: Stripped background-clip to prevent transparency bugs)
st.markdown("""
    <div class="hero-container" style="text-align: center; padding: 2.5rem 1rem 1.5rem 1rem; background: linear-gradient(135deg, rgba(31,18,54,0.6) 0%, rgba(15,10,28,0.6) 100%); border-radius: 16px; border: 1px solid rgba(147, 51, 234, 0.2); margin-bottom: 2.5rem; box-shadow: 0 8px 32px 0 rgba(147, 51, 234, 0.05);">
        <h1 style="color: #ffffff !important; font-family: 'Inter', sans-serif !important; font-size: 42px !important; font-weight: 800 !important; margin: 0px !important; letter-spacing: -0.5px !important; text-shadow: 0px 0px 15px rgba(168, 85, 247, 0.65);">     Customer AI Data Analyst Assistant</h1>
        <p style="color: #94a3b8 !important; font-family: 'Inter', sans-serif !important; font-size: 16px !important; margin-top: 12px !important; margin-bottom: 0px !important; font-weight: 400 !important;">⚡ Premium Business Intelligence Platform with Groq AI & Predictive Inference Models</p>
    </div>
""", unsafe_allow_html=True)

# 4. File Upload Area
file = st.file_uploader("Upload Customer Sales Dataset (CSV or XLSX)", type=["csv", "xlsx"])

if file:
    df_raw = load_file(file)

    st.markdown('<p class="section-header">📋 Raw Ingested Data Preview</p>', unsafe_allow_html=True)
    st.dataframe(df_raw.head(5), use_container_width=True)

    # Core data cleaning execution loop
    df = clean_dataset(df_raw)

    st.markdown('<p class="section-header">✨ Cleaned & Standardized Dataset</p>', unsafe_allow_html=True)
    st.dataframe(df.head(5), use_container_width=True)

    st.markdown('<p class="section-header">📊 Financial Performance Highlights</p>', unsafe_allow_html=True)
    kpis = generate_kpis(df)
    
    kpi_cols = st.columns(4)
    with kpi_cols[0]: st.metric("Total Revenue Generated", f"${kpis['total_revenue']:,}")
    with kpi_cols[1]: st.metric("Total Operational Cost", f"${kpis['total_cost']:,}")
    with kpi_cols[2]: st.metric("Net Profit Margin", f"${kpis['total_profit']:,}")
    with kpi_cols[3]: st.metric("Transactions Processed", f"{kpis['total_rows']:,}")

    st.markdown("---")

    # Render Visual Dashboard Plots
    show_dashboard(df)

    st.markdown("---")

    # Executive Diagnostics Form Container
    st.markdown('<p class="section-header">💡 Automated Executive AI Insights</p>', unsafe_allow_html=True)
    with st.container():
        if st.button("Run AI Insights Diagnostics"):
            with st.spinner("Streaming context vectors to Groq Cloud..."):
                result = get_insights(df)
                st.write(result)

    st.markdown("---")

    # Conversational Chat Form Container
    st.markdown('<p class="section-header">💬 Conversational Data Assistant Chat</p>', unsafe_allow_html=True)
    with st.form(key="chatbot_form", clear_on_submit=False):
        question = st.text_input("Ask a targeted business question (e.g., 'Which product category has the highest margins?'):")
        submit_chat = st.form_submit_button(label="Ask Assistant")
        
    if submit_chat and question:
        with st.spinner("Evaluating data frame context parameters..."):
            answer = chat_with_data(df, question)
            st.info(answer)

    st.markdown("---")

    # Machine Learning / Predictive Inference Container
    st.markdown('<p class="section-header">🔮 Predictive Revenue Forecasting Matrix</p>', unsafe_allow_html=True)
    num_cols = df.select_dtypes(include="number").columns.tolist()
    valid_ml_cols = [c for c in num_cols if 'id' not in c.lower()]

    if len(valid_ml_cols) >= 2:
        with st.form(key="prediction_model_form"):
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                x_var = st.selectbox("Independent Predictor Variable (X)", valid_ml_cols, index=0)
            with p_col2:
                y_var = st.selectbox("Dependent Target Variable (Y)", valid_ml_cols, index=min(1, len(valid_ml_cols)-1))
            
            submit_prediction = st.form_submit_button("Train & Run Prediction Model")
        
        if submit_prediction:
            run_prediction(df, x_var, y_var)
    else:
        st.info("Insufficient continuous numeric vectors found to run regression models.")