# QuantResearchStarter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/username/QuantResearchStarter/actions/workflows/ci.yml/badge.svg)](https://github.com/username/QuantResearchStarter/actions)

A modular, open-source quantitative research and backtesting framework built for clarity, reproducibility, and extensibility. Ideal for researchers, students, and engineers building and testing systematic strategies.

---

## Why this project

QuantResearchStarter provides a clean, well-documented starting point for quantitative research and backtesting. Its priorities are:

* **Readability**: idiomatic Python, type hints, and small modules you can read and change quickly.
* **Testability**: deterministic vectorized backtests with unit tests and CI.
* **Extensibility**: plugin-friendly factor & data adapters so you can try new ideas fast.

---

## Features

* **Data management** — download market data or generate synthetic price series for experiments.
* **Factor library** — example implementations of momentum, value, size, and volatility factors.
* **Vectorized backtesting engine** — supports transaction costs, slippage, and portfolio constraints.
* **Risk & performance analytics** — returns, drawdowns, Sharpe, turnover, and other risk metrics.
* **CLI & scripts** — small tools to generate data, compute factors, and run backtests from the terminal.
* **Production-ready utilities** — type hints, tests, continuous integration, and documentation scaffolding.

---

## Quick start

### Requirements

* Python 3.10+
* pip

### Install locally

```bash
# Clone the repository
git clone https://github.com/username/QuantResearchStarter.git
cd QuantResearchStarter

# Install package in development mode
pip install -e .

# Install development dependencies (tests, linters, docs)
pip install -e ".[dev]"

# Optional UI dependencies
pip install streamlit plotly
```

### Demo (one-line)

```bash
make demo
```

### Step-by-step demo

```bash
# generate synthetic sample price series
qrs generate-data -o data_sample/sample_prices.csv -s 5 -d 365

# compute example factors
qrs compute-factors -d data_sample/sample_prices.csv -f momentum -f value -o output/factors.csv

# run a backtest
qrs backtest -d data_sample/sample_prices.csv -s output/factors.csv -o output/backtest_results.json

# optional: start the Streamlit dashboard
streamlit run src/quant_research_starter/dashboard/streamlit_app.py
```

---

## Minimal example

```python
from quant_research_starter.backtest import Backtester
from quant_research_starter.data import load_prices
from quant_research_starter.factors import Momentum

prices = load_prices("data_sample/sample_prices.csv")
factor = Momentum(window=63)
scores = factor.compute(prices)

bt = Backtester(prices, signals=scores, capital=1_000_000)
results = bt.run()
print(results.performance.summary())
```

> See the `examples/` directory for fully working notebooks and scripts.

---

## CLI reference

Run `qrs --help` or `qrs <command> --help` for full usage. Main commands include:

* `qrs generate-data` — create synthetic price series or download data from adapters
* `qrs compute-factors` — calculate and export factor scores
* `qrs backtest` — run the vectorized backtest and export results

---

## Project structure (overview)

```
QuantResearchStarter/
├─ src/quant_research_starter/
│  ├─ data/              # data loaders & adapters
│  ├─ factors/           # factor implementations
│  ├─ backtest/          # backtester & portfolio logic
│  ├─ analytics/         # performance and risk metrics
│  ├─ cli/               # command line entry points
│  └─ dashboard/         # optional Streamlit dashboard
├─ examples/             # runnable notebooks & example strategies
├─ tests/                # unit + integration tests
└─ docs/                 # documentation source
```

---

## Tests & CI

Run unit tests locally with:

```bash
pytest -q
```

CI runs linting (ruff), formatting checks (black), and unit tests across supported Python versions. The workflow is defined in `.github/workflows/ci.yml`.

---

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a descriptive branch (feature or fix)
3. Add tests for new behavior
4. Open a pull request with a clear description and rationale

Before submitting, ensure your tests pass and formatting/linting checks succeed.

---

## AI policy (short & practical)

**Yes — you may use AI tools** (ChatGPT, Copilot, etc.) to help write or review code and documentation. Please follow these guidelines:

* **Disclose** substantial AI assistance in the PR or commit message (e.g., "Generated with ChatGPT; reviewed and adapted by @your-username").
* **Review thoroughly** all AI-generated code for correctness, security, numerical stability, and licensing concerns.
* **Add tests** for AI-generated logic when applicable.
* **Respect licenses**: do not paste or rely on large verbatim copyrighted snippets without appropriate permission or attribution.

This policy encourages fast iteration while maintaining quality and transparency.

---

## License

This project is available under the MIT License — see the `LICENSE` file for details.

---
