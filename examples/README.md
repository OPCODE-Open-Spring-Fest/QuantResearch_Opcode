### Examples

Run a full demo with sample data:

```bash
make demo
```

Or step-by-step:

```bash
qrs generate-data -o data_sample/sample_prices.csv -s 5 -d 365
qrs compute-factors -d data_sample/sample_prices.csv -f momentum -f value -o output/factors.csv
qrs backtest -d data_sample/sample_prices.csv -s output/factors.csv -o output/backtest_results.json
```



