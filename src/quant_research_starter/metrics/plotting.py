"""Plotting utilities for backtest results."""

from pathlib import Path
from typing import List

import pandas as pd

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

import matplotlib.pyplot as plt


def create_equity_curve_plot(
    dates: List[str],
    portfolio_values: List[float],
    initial_capital: float,
    output_path: str,
    plot_type: str = "png"
) -> str:
    """
    Create equity curve plot in specified format.
    Args:
        dates: List of date strings
        portfolio_values: List of portfolio values
        initial_capital: Starting capital
        output_path: Path to save the plot
        plot_type: 'png' for matplotlib, 'html' for plotly

    Returns:
        Path to saved file
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    dates = pd.to_datetime(dates)
    portfolio_series = pd.Series(portfolio_values, index=dates)
    if plot_type == "html" and PLOTLY_AVAILABLE:
        return _create_plotly_chart(portfolio_series, initial_capital, output_path)
    else:
        return _create_matplotlib_chart(portfolio_series, output_path)
def _create_plotly_chart(
    portfolio_series: pd.Series,
    initial_capital: float,
    output_path: str
) -> str:
    """Create interactive Plotly HTML chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=portfolio_series.index,
        y=portfolio_series.values,
        mode='lines',
        name='Portfolio Value',
        line={'color': '#2E86AB', 'width': 3},
        hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Value</b>: $%{y:,.2f}<extra></extra>'
    ))
    # Add initial capital reference line
    fig.add_hline(
        y=initial_capital,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Initial Capital: ${initial_capital:,.0f}",
        annotation_position="bottom right"
    )
    total_return_pct = ((portfolio_series.iloc[-1] / initial_capital) - 1) * 10
    fig.update_layout(
        title=f"Backtest Performance (Total Return: {total_return_pct:+.1f}%)",
        xaxis_title='Date',
        yaxis_title='Portfolio Value ($)',
        template='plotly_white',
        hovermode='x unified',
        height=500
    )
    fig.update_yaxes(tickprefix='$', tickformat=',.0f')
    fig.write_html(output_path)
    return output_path
def _create_matplotlib_chart(portfolio_series: pd.Series, output_path: str) -> str:
    """Create static matplotlib PNG chart."""
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_series.index, portfolio_series.values, linewidth=2)
    plt.title('Portfolio Value')
    plt.ylabel('USD')
    plt.grid(True, alpha=0.3)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return output_path
