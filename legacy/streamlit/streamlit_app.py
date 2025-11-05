import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Quant Research Starter", layout="wide")
st.title("📊 Quant Research Starter Dashboard")
output_dir = Path.cwd() / "output"
default_results = output_dir / "backtest_results.json"
default_factors = output_dir / "factors.csv"

# --- Sidebar Inputs ---
st.sidebar.header("⚙️ Inputs")
results_file = st.sidebar.text_input("Backtest results JSON", str(default_results))
factors_file = st.sidebar.text_input("Factors CSV", str(default_factors))

# --- Main Layout ---
st.markdown("### Overview")
st.caption("Visualize portfolio performance and factor signals side-by-side.")

# Create two balanced columns
col1, col2 = st.columns([1, 1], gap="large")

# --- Left: Equity Curve ---
with col1:
    st.markdown("#### 📈 Equity Curve")
    if Path(results_file).exists():
        with open(results_file) as f:
            data = json.load(f)

        df = pd.DataFrame(
            {
                "date": pd.to_datetime(data["dates"]),
                "portfolio_value": data["portfolio_value"],
            }
        ).set_index("date")

        fig = px.line(
            df,
            y="portfolio_value",
            title="Portfolio Value Over Time",
            labels={"portfolio_value": "Portfolio Value"},
        )
        fig.update_layout(
            margin={"l": 30, "r": 30, "t": 40, "b": 30},
            height=400,
            title_x=0.5,
        )

        st.plotly_chart(fig, use_container_width=True)

        # Centered metrics section
        st.markdown("#### 🔍 Summary Metrics")
        metrics = data.get("metrics", {})
        if metrics:
            mcol1, mcol2, mcol3 = st.columns(3)
            items = list(metrics.items())
            for i, (key, value) in enumerate(items[:3]):
                with [mcol1, mcol2, mcol3][i]:
                    st.metric(
                        label=key.replace("_", " ").title(), value=round(value, 4)
                    )
            if len(items) > 3:
                st.json(dict(items[3:]))
        else:
            st.info("No metrics found in results.")
    else:
        st.info("⚠️ Run the CLI backtest to generate results.")

# --- Right: Factor Signals ---
with col2:
    st.markdown("#### 📉 Factor Signals")
    if Path(factors_file).exists():
        fdf = pd.read_csv(factors_file, index_col=0, parse_dates=True)

        # Tabs for cleaner organization
        tab1, tab2 = st.tabs(["📑 Latest Data", "📊 Composite Signal"])

        with tab1:
            st.dataframe(
                fdf.tail().style.set_table_styles(
                    [{"selector": "th", "props": [("text-align", "center")]}]
                )
            )

        with tab2:
            if "composite" in fdf.columns:
                fig2 = px.line(
                    fdf[["composite"]],
                    title="Composite Factor Signal",
                    labels={"composite": "Composite"},
                )
                fig2.update_layout(
                    margin={"l": 30, "r": 30, "t": 40, "b": 30},
                    height=400,
                    title_x=0.5,
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No composite signal found.")
    else:
        st.info("⚠️ Compute factors to view signals.")

# --- Footer ---
st.markdown("---")
st.caption(
    "💡 Tip: Use `qrs` CLI to generate data, factors, and backtest results, then refresh this page."
)
