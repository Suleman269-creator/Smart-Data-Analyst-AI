# ⚡ QuikBI Analyst

An advanced, enterprise-grade AI Business Intelligence (BI) and Automated Insights platform. **QuikBI Analyst** normalizes heavily contaminated transactional sales data, generates real-time performance dashboards, executes machine learning revenue forecasting, and uses conversational generative AI engines to deliver executive-level corporate diagnostics.

🚀 **Live Production Workspace:** [smart-data-analyst-ai.streamlit.app](https://smart-data-analyst-ai-tv2mdjwdwdg68vau2sjojx.streamlit.app/)

---

## ✨ System Architecture & Core Modules

The platform is designed using an optimized, decoupled pipeline architecture where data transformation, analytics, and intelligence execution are strictly isolated across dedicated functional sub-engines:

* **`app.py`:** The main portal interface orchestration engine. Manages premium custom CSS glassmorphic view grids, component state retention, and responsive UI rendering.
* **`modules/loader.py`:** Secure file system input processing layer designed to natively decode dynamic `.csv` and `.xlsx` multi-year workbook streams.
* **`modules/cleaner.py`:** An aggressive regex preprocessing sub-engine. It standardizes mixed string-and-integer vectors, strips currency noise (`$`, `Rs.`, commas), standardizes lower snake_case headers, and replaces ambiguous text null values with professional `"Uncategorized"` tags.
* **`modules/analyzer.py`:** Aggregates cross-vector matrix values into live corporate performance metrics (Revenue, Cost, Profit Margins, Order Volume).
* **`modules/visualizer.py`:** Renders highly interactive visualizations including financial margin comparisons and revenue-weighted tree-maps.
* **`modules/ai_engine.py`:** Orchestrates zero-latency executive-level analytical summaries by feeding pre-computed python metadata frames into the **Llama-3.1-8b-Instant** model via the **Groq API Gateway**.
* **`modules/chatbot.py`:** A conversational text layout engine allowing corporate users to query raw tables using standard human prose.
* **`modules/predictor.py`:** An Automated Machine Learning (AutoML) panel running background statistical regression modeling for time-series forward-looking business forecasting.

---

## 🛠️ The Professional Technical Stack

* **User Interface Framework:** `Streamlit` (Injected with advanced inline CSS/HTML styling)
* **Data Transformation Processing:** `Pandas` | `NumPy`
* **Interactive Graphic Visualizations:** `Plotly Express` | `Plotly Graph Objects`
* **Inference Compute Infrastructure:** `Groq Cloud SDK` (Model: `llama-3.1-8b-instant`)
* **Predictive Modeling Core:** `Scikit-Learn` (Regression Forecasting Engine)
* **Spreadsheet Parsing Extension:** `openpyxl`

---

## 📁 Repository Structural Blueprint

```text
Smart-Data-Analyst-AI/
│
├── .streamlit/
│   └── secrets.toml          # Local secret configurations (SAFEGUARDED BY GITIGNORE)
│
├── modules/
│   ├── loader.py             # File ingestion utility
│   ├── cleaner.py            # Custom regex string-cleansing logic
│   ├── analyzer.py           # Global corporate KPI aggregator
│   ├── visualizer.py         # Advanced Plotly graphing script
│   ├── ai_engine.py          # Groq context builder for diagnostics
│   ├── chatbot.py            # Conversational table chat model orchestration
│   └── predictor.py          # Machine learning predictive forecasting matrix
│
├── app.py                    # Main dashboard rendering application portal
├── logo.png                  # Background-removed QuikBI transparent branding image
├── requirements.txt          # Explicit production library dependencies listing
├── .gitignore                # Target tracking version-control exclusions list
└── README.md                 # System deployment manual and architecture guide