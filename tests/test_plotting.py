import os

from quant_research_starter.metrics.plotting import create_equity_curve_plot


def test_plotly_html_creation():
    # Create test data matching the backtest results structure
    dates = [f"2020-01-{i + 1:02d}" for i in range(20)]
    portfolio_values = [1000000 + i * 5000 for i in range(20)]

    # Test HTML creation
    test_html_path = "test_output/backtest_plot.html"
    html_path = create_equity_curve_plot(
        dates=dates,
        portfolio_values=portfolio_values,
        initial_capital=1000000,
        output_path=test_html_path,
        plot_type="html",
    )

    # Verify file was created
    assert os.path.exists(html_path)
    assert html_path.endswith(".html")
    assert os.path.getsize(html_path) > 1000

    # Cleanup
    if os.path.exists(html_path):
        os.remove(html_path)
    if os.path.exists("test_output"):
        os.rmdir("test_output")


def test_plotly_fallback_to_matplotlib():
    """Test that PNG is created even if Plotly is not available."""
    dates = [f"2020-01-{i + 1:02d}" for i in range(15)]
    portfolio_values = [1000000 + i * 3000 for i in range(15)]

    # Test PNG creation
    test_png_path = "test_output/backtest_plot.png"
    png_path = create_equity_curve_plot(
        dates=dates,
        portfolio_values=portfolio_values,
        initial_capital=1000000,
        output_path=test_png_path,
        plot_type="png",
    )

    assert os.path.exists(png_path)
    assert png_path.endswith(".png")

    # Cleanup
    if os.path.exists(png_path):
        os.remove(png_path)
    if os.path.exists("test_output"):
        os.rmdir("test_output")
