PY=python

.PHONY: install dev test lint format demo precommit

install:
	$(PY) -m pip install --upgrade pip
	pip install -e .

dev:
	pip install -e .[dev]
	pre-commit install

test:
	pytest -q

lint:
	ruff check src/ tests/
	black --check src/ tests/

format:
	black src/ tests/
	ruff check --fix src/ tests/

demo:
	$(PY) -m quant_research_starter.cli generate-data -o data_sample/sample_prices.csv -s 5 -d 365
	$(PY) -m quant_research_starter.cli compute-factors -d data_sample/sample_prices.csv -f momentum -f value -o output/factors.csv
	$(PY) -m quant_research_starter.cli backtest -d data_sample/sample_prices.csv -s output/factors.csv -o output/backtest_results.json

precommit:
	pre-commit run --all-files



