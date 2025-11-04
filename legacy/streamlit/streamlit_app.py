import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Quant Research Starter", layout="wide")
st.title("Quant Research Starter Dashboard")

output_dir = Path.cwd() / "output"
default_results = output_dir / "backtest_results.json"
default_factors = output_dir / "factors.csv"

st.sidebar.header("Inputs")
results_file = st.sidebar.text_input("Backtest results JSON", str(default_results))
factors_file = st.sidebar.text_input("Factors CSV", str(default_factors))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Equity Curve")
    if Path(results_file).exists():
        with open(results_file) as f:
            data = json.load(f)
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(data["dates"]),
                "portfolio_value": data["portfolio_value"],
            }
        ).set_index("date")
        fig = px.line(df, y="portfolio_value", title="Portfolio Value")
        st.plotly_chart(fig, use_container_width=True)
        st.json(data.get("metrics", {}))
    else:
        st.info("Run the CLI backtest to generate results.")

with col2:
    st.subheader("Factor Signals")
    if Path(factors_file).exists():
        fdf = pd.read_csv(factors_file, index_col=0, parse_dates=True)
        st.dataframe(fdf.tail())
        if "composite" in fdf.columns:
            fig2 = px.line(fdf[["composite"]], title="Composite Signal")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Compute factors to view signals.")

st.markdown("---")
st.caption(
    "Tip: Use qrs CLI to generate data, factors, and backtest results. Then refresh this page."
)
