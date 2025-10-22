---
name: "Good First Issue: Add Plotly PnL chart to CLI"
about: Enhance CLI to output interactive Plotly HTML chart
labels: good-first-issue
---

### Summary
Modify CLI backtest command to also save a Plotly HTML chart for PnL.

### Tasks
- Use Plotly to create an interactive equity curve.
- Save to `output/backtest_plot.html`.
- Add a unit smoke test that the file is created.

### Definition of Done
- CLI still supports Matplotlib PNG; Plotly HTML added.


