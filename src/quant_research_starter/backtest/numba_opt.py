"""Numba-accelerated backtest operations."""

import numpy as np

try:
    from numba import jit, prange

    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False

    def jit(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    prange = range


@jit(nopython=True, cache=True)
def compute_strategy_returns(
    weights_prev: np.ndarray,
    returns: np.ndarray,
    turnover: np.ndarray,
    transaction_cost: float,
) -> np.ndarray:
    """Compute strategy returns with transaction costs."""
    n_days, n_assets = returns.shape
    strat_ret = np.zeros(n_days)

    for i in prange(n_days):
        ret_sum = 0.0
        for j in prange(n_assets):
            ret_sum += weights_prev[i, j] * returns[i, j]
        strat_ret[i] = ret_sum - (turnover[i] * transaction_cost)

    return strat_ret


@jit(nopython=True, cache=True)
def compute_turnover(weights: np.ndarray, weights_prev: np.ndarray) -> np.ndarray:
    """Compute turnover (L1 change / 2)."""
    n_days, n_assets = weights.shape
    turnover = np.zeros(n_days)

    for i in prange(n_days):
        total_change = 0.0
        for j in prange(n_assets):
            total_change += abs(weights[i, j] - weights_prev[i, j])
        turnover[i] = total_change * 0.5

    return turnover


@jit(nopython=True, cache=True)
def compute_portfolio_value(
    strategy_returns: np.ndarray, initial_capital: float
) -> np.ndarray:
    """Compute cumulative portfolio value."""
    n_days = len(strategy_returns)
    portfolio_value = np.zeros(n_days + 1)
    portfolio_value[0] = initial_capital

    for i in prange(n_days):
        portfolio_value[i + 1] = portfolio_value[i] * (1.0 + strategy_returns[i])

    return portfolio_value[1:]


@jit(nopython=True, cache=True)
def compute_returns_from_prices(prices: np.ndarray) -> np.ndarray:
    """Compute percentage returns from prices."""
    n_days, n_assets = prices.shape
    returns = np.zeros((n_days - 1, n_assets))

    for i in prange(n_days - 1):
        for j in prange(n_assets):
            if prices[i, j] > 0:
                returns[i, j] = (prices[i + 1, j] - prices[i, j]) / prices[i, j]

    return returns


@jit(nopython=True, cache=True)
def rank_based_weights(
    signals: np.ndarray, max_leverage: float, long_pct: float, short_pct: float
) -> np.ndarray:
    """Compute rank-based portfolio weights."""
    n_assets = len(signals)
    weights = np.zeros(n_assets)

    valid_mask = np.zeros(n_assets, dtype=np.bool_)
    n_valid = 0
    for i in range(n_assets):
        if not np.isnan(signals[i]):
            valid_mask[i] = True
            n_valid += 1

    if n_valid == 0:
        return weights

    valid_values = np.zeros(n_valid)
    valid_indices = np.zeros(n_valid, dtype=np.int64)
    idx = 0
    for i in range(n_assets):
        if valid_mask[i]:
            valid_values[idx] = signals[i]
            valid_indices[idx] = i
            idx += 1

    sorted_idx = np.argsort(valid_values)
    ranks = np.zeros(n_valid)
    for i in range(n_valid):
        ranks[sorted_idx[i]] = i + 1.0

    sorted_ranks = np.sort(ranks)
    long_idx = int(n_valid * long_pct)
    short_idx = int(n_valid * short_pct)
    long_threshold = sorted_ranks[long_idx] if long_idx < n_valid else sorted_ranks[-1]
    short_threshold = sorted_ranks[short_idx] if short_idx >= 0 else sorted_ranks[0]

    long_count = 0
    short_count = 0

    for idx in range(n_valid):
        i = valid_indices[idx]
        rank_val = ranks[idx]
        if rank_val >= long_threshold:
            weights[i] = 1.0
            long_count += 1
        elif rank_val <= short_threshold:
            weights[i] = -1.0
            short_count += 1

    if long_count > 0:
        long_weight = 1.0 / long_count
        for i in range(n_assets):
            if weights[i] > 0:
                weights[i] = long_weight
    if short_count > 0:
        short_weight = -1.0 / short_count
        for i in range(n_assets):
            if weights[i] < 0:
                weights[i] = short_weight

    total_leverage = 0.0
    for i in range(n_assets):
        total_leverage += abs(weights[i])

    if total_leverage > max_leverage and total_leverage > 0:
        scale = max_leverage / total_leverage
        for i in range(n_assets):
            weights[i] *= scale

    return weights
