---
name: "Good First Issue: Add weekly/monthly rebalancing option"
about: Add `rebalance_freq` support to `VectorizedBacktest`
labels: good-first-issue
---

### Summary
Teach `VectorizedBacktest` to rebalance weekly or monthly via a `rebalance_freq` parameter.

### Tasks
- Update `_should_rebalance` to respect `W` and `M` frequencies.
- Add tests in `tests/test_backtest.py`.
- Document in README.

### Definition of Done
- Tests pass; daily default unchanged.
