# QuantResearchStarter

A modular, open-source quantitative research and backtesting framework designed for clarity and extensibility. Perfect for researchers, students, and developers interested in quantitative finance.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![CI](https://github.com/username/QuantResearchStarter/actions/workflows/ci.yml/badge.svg)](https://github.com/username/QuantResearchStarter/actions)

## Features

- **Data Management**: Download real data or generate synthetic data for testing
- **Factor Library**: Implement momentum, value, size, and volatility factors
- **Backtesting Engine**: Vectorized backtester with transaction costs and constraints
- **Risk Metrics**: Comprehensive performance and risk analytics
- **Modular Design**: Easy to extend with new factors and strategies
- **Production Ready**: Type hints, tests, CI/CD, and documentation

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/username/QuantResearchStarter.git
cd QuantResearchStarter

# Install package in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Optional UI
pip install streamlit plotly
```

### Quick Demo

```bash
make demo
```

Or step-by-step:

```bash
qrs generate-data -o data_sample/sample_prices.csv -s 5 -d 365
qrs compute-factors -d data_sample/sample_prices.csv -f momentum -f value -o output/factors.csv
qrs backtest -d data_sample/sample_prices.csv -s output/factors.csv -o output/backtest_results.json

# Streamlit dashboard (optional)
streamlit run src/quant_research_starter/dashboard/streamlit_app.py
```
