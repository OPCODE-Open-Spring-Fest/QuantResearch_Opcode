# QuantResearchStarter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/username/QuantResearchStarter/actions/workflows/ci.yml/badge.svg)](https://github.com/username/QuantResearchStarter/actions)

A modular, open-source quantitative research and backtesting framework built for clarity, reproducibility, and extensibility. Ideal for researchers, students, and engineers building and testing systematic strategies.

---

## Why this project

QuantResearchStarter aims to provide a clean, well-documented starting point for quantitative research and backtesting. It focuses on:

* **Readability**: idiomatic Python, type hints, and small modules you can read and change quickly.
* **Testability**: deterministic vectorized backtests with unit tests and CI.
* **Extensibility**: plug-in friendly factor & data adapters so you can try new ideas fast.

---

## Key features

* **Data management** — download market data or generate synthetic price series for experiments.
* **Factor library** — example implementations of momentum, value, size, and volatility factors.
* **Vectorized backtesting engine** — supports transaction costs, slippage, portfolio constraints, and configurable rebalancing frequencies (daily, weekly, monthly).
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

### Quick CLI Usage

After installation, you can use the CLI in two ways:

**Option 1: Direct command (if PATH is configured)**
```bash
qrs --help
python -m quant_research_starter.cli generate-data -o data_sample/sample_prices.csv -s 5 -d 365
python -m quant_research_starter.cli compute-factors -d data_sample/sample_prices.csv -f momentum -f value -o output/factors.csv
qrs backtest -d data/sample.csv -s output/factors.csv
```

**Option 2: Python module (always works)**
```bash
python -m quant_research_starter.cli --help
python -m quant_research_starter.cli generate-data -o data/sample.csv -s 5 -d 365
python -m quant_research_starter.cli compute-factors -d data/sample.csv -f momentum -f value
python -m quant_research_starter.cli backtest -d data_sample/sample_prices.csv -s output/factors.csv -o output/backtest_results.json
```

### Demo (one-line)

```bash
make demo
```

### Step-by-step demo

```bash
# generate synthetic sample price series
python -m quant_research_starter.cli generate-data -o data_sample/sample_prices.csv -s 5 -d 365

# compute example factors
python -m quant_research_starter.cli compute-factors -d data_sample/sample_prices.csv -f momentum -f value -o output/factors.csv

# run a backtest
python -m quant_research_starter.cli backtest -d data_sample/sample_prices.csv -s output/factors.csv -o output/backtest_results.json

# optional: start the Streamlit dashboard
streamlit run src/quant_research_starter/dashboard/streamlit_app.py
```

---

## Example: small strategy (concept)

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

### Rebalancing Frequency

The backtester supports different rebalancing frequencies to match your strategy needs:

```python
from quant_research_starter.backtest import VectorizedBacktest

# Daily rebalancing (default)
bt_daily = VectorizedBacktest(prices, signals, rebalance_freq="D")

# Weekly rebalancing (reduces turnover and transaction costs)
bt_weekly = VectorizedBacktest(prices, signals, rebalance_freq="W")

# Monthly rebalancing (lowest turnover)
bt_monthly = VectorizedBacktest(prices, signals, rebalance_freq="M")

results = bt_monthly.run()
```

Supported frequencies:
- `"D"`: Daily rebalancing (default)
- `"W"`: Weekly rebalancing (rebalances when the week changes)
- `"M"`: Monthly rebalancing (rebalances when the month changes)

> The code above is illustrative—see `examples/` for fully working notebooks and scripts.

---

## CLI reference

Run `python -m quant_research_starter.cli --help` or `python -m quant_research_starter.cli <command> --help` for full usage. Main commands include:

* `python -m quant_research_starter.cli generate-data` — create synthetic price series or download data from adapters
* `python -m quant_research_starter.cli compute-factors` — calculate and export factor scores
* `python -m quant_research_starter.cli backtest` — run the vectorized backtest and export results

**Note:** If you have the `qrs` command in your PATH, you can use `qrs` instead of `python -m quant_research_starter.cli`.

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

We include unit tests and a CI workflow (GitHub Actions). Run tests locally with:

```bash
pytest -q
```

The CI pipeline runs linting, unit tests, and builds docs on push/PR.

---

## Contributing

Contributions are very welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Add tests for new behavior
4. Open a pull request with a clear description and rationale

Please review `CONTRIBUTING.md` and the `CODE_OF_CONDUCT.md` before submitting.

---

## AI policy — short & practical

**Yes — you are allowed to use AI tools** (ChatGPT, Copilot, Codeium, etc.) to help develop, prototype, or document code in this repository.

A few friendly guidelines:

* **Be transparent** when a contribution is substantially generated by an AI assistant — add a short note in the PR or commit message (e.g., "Generated with ChatGPT; reviewed and adapted by <your-name>").
* **Review and test** all AI-generated code. Treat it as a helpful draft, not final production-quality code.
* **Follow licensing** and attribution rules for any external snippets the AI suggests. Don’t paste large verbatim copyrighted material.
* **Security & correctness**: double-check numerical logic, data handling, and anything that affects trading decisions.

This policy is intentionally permissive: we want the community to move fast while keeping quality and safety in mind.

---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

---

## Acknowledgements

Built with inspiration from open-source quant libraries and the research community. If you use this project in papers or public work, a short citation or mention is appreciated.
