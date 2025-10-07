---
name: "Good First Issue: Add Bollinger Bands factor"
about: Implement a simple Bollinger Bands factor example
labels: good-first-issue
---

### Summary
Add a new example factor `BollingerBandsFactor` under `src/quant_research_starter/factors/`.

### Tasks
- Create `bollinger.py` with a factor computing z-score of price vs. rolling band.
- Export in `factors/__init__.py`.
- Add unit tests in `tests/test_factors.py`.
- Update README with a short mention.

### Definition of Done
- `pytest` passes and coverage unchanged or better.

---
name: "Good First Issue: Add New Simple Factor"
title: "Factor Implementation: [Your Factor Name]"
labels: ["good-first-issue", "enhancement", "factors"]
assignees: []
---

## Description
Add a new factor implementation to the factors module. This is a great first issue to understand how factors work in the framework.

## Suggested Factor
**Factor Name**: Liquidity Factor  
**Description**: Measure trading liquidity using volume-based metrics

## Implementation Steps
1. Create new file `src/quant_research_starter/factors/liquidity.py`
2. Implement a `LiquidityFactor` class inheriting from `Factor`
3. Use trading volume (or synthetic volume) to compute liquidity measures
4. Add basic tests in `tests/test_factors.py`
5. Update `src/quant_research_starter/factors/__init__.py` to export the new factor

## Code Example
```python
class LiquidityFactor(Factor):
    def compute(self, prices: pd.DataFrame, volumes: pd.DataFrame = None) -> pd.DataFrame:
        # Your implementation here
        # Suggested: Use dollar volume or turnover as liquidity proxy
        pass