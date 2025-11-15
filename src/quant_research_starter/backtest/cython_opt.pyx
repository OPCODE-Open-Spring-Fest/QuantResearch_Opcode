"""Cython-optimized backtest operations (skeleton)."""

cimport cython
import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t


@cython.boundscheck(False)
@cython.wraparound(False)
def compute_strategy_returns_cython(
    np.ndarray[DTYPE_t, ndim=2] weights_prev,
    np.ndarray[DTYPE_t, ndim=2] returns,
    np.ndarray[DTYPE_t, ndim=1] turnover,
    DTYPE_t transaction_cost
):
    """Compute strategy returns with transaction costs (Cython version)."""
    cdef int n_days = weights_prev.shape[0]
    cdef int n_assets = weights_prev.shape[1]
    cdef np.ndarray[DTYPE_t, ndim=1] strat_ret = np.zeros(n_days, dtype=DTYPE)
    cdef int i, j
    cdef DTYPE_t ret_sum
    
    for i in range(n_days):
        ret_sum = 0.0
        for j in range(n_assets):
            ret_sum += weights_prev[i, j] * returns[i, j]
        strat_ret[i] = ret_sum - (turnover[i] * transaction_cost)
    
    return strat_ret


@cython.boundscheck(False)
@cython.wraparound(False)
def compute_turnover_cython(
    np.ndarray[DTYPE_t, ndim=2] weights,
    np.ndarray[DTYPE_t, ndim=2] weights_prev
):
    """Compute turnover (L1 change / 2) (Cython version)."""
    cdef int n_days = weights.shape[0]
    cdef int n_assets = weights.shape[1]
    cdef np.ndarray[DTYPE_t, ndim=1] turnover = np.zeros(n_days, dtype=DTYPE)
    cdef int i, j
    cdef DTYPE_t total_change
    
    for i in range(n_days):
        total_change = 0.0
        for j in range(n_assets):
            total_change += abs(weights[i, j] - weights_prev[i, j])
        turnover[i] = total_change * 0.5
    
    return turnover

