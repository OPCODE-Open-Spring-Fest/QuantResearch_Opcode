FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src

RUN pip install --upgrade pip && pip install -e .[dev]

CMD ["bash", "-lc", "pytest -q && python -m quant_research_starter.cli backtest -d data_sample/sample_prices.csv -o output/backtest_results.json --no-plot || true && ls -la output || true"]



