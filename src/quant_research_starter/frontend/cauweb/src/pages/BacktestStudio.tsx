import React, { useState } from 'react';
import { Play, TrendingUp, TrendingDown, Target, DollarSign, Calendar, BarChart3, Activity } from 'lucide-react';
import { PerformanceChart } from '../components/PerformanceChart';

interface BacktestMetrics {
  totalReturn: number;
  annualizedReturn: number;
  volatility: number;
  sharpeRatio: number;
  maxDrawdown: number;
  winRate: number;
  turnover: number;
  profitFactor: number;
  sortinoRatio: number;
  calmarRatio: number;
}

interface Trade {
  symbol: string;
  quantity: number;
  price: number;
  timestamp: string;
  side: 'BUY' | 'SELL';
  pnl: number;
}

export const BacktestStudio: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [backtestResults, setBacktestResults] = useState<{
    metrics: BacktestMetrics;
    trades: Trade[];
    portfolioHistory: { date: string; value: number }[];
    benchmarkHistory: { date: string; value: number }[];
  } | null>(null);
  
  const [config, setConfig] = useState({
    initialCapital: 100000,
    startDate: '2020-01-01',
    endDate: '2023-12-31',
    rebalanceFrequency: 'monthly',
    strategy: 'momentum',
    symbols: ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA']
  });

  const handleRunBacktest = async () => {
    setLoading(true);
    
    // Simulate API call with realistic delay
    await new Promise(resolve => setTimeout(resolve, 2500));
    
    // Generate mock data
    const mockResults = {
      metrics: {
        totalReturn: 0.2345,
        annualizedReturn: 0.0876,
        volatility: 0.1567,
        sharpeRatio: 1.234,
        maxDrawdown: 0.1234,
        winRate: 0.645,
        turnover: 2.34,
        profitFactor: 1.89,
        sortinoRatio: 1.567,
        calmarRatio: 0.707
      },
      trades: generateMockTrades(),
      portfolioHistory: generatePortfolioHistory(),
      benchmarkHistory: generateBenchmarkHistory()
    };
    
    setBacktestResults(mockResults);
    setLoading(false);
  };

  const getMetrics = () => {
    if (!backtestResults?.metrics) return [];
    
    const metrics = backtestResults.metrics;
    return [
      { 
        key: 'Total Return', 
        value: `${(metrics.totalReturn * 100).toFixed(2)}%`,
        change: `${(metrics.annualizedReturn * 100).toFixed(2)}% annualized`,
        icon: TrendingUp,
        trend: metrics.totalReturn > 0 ? 'positive' : 'negative',
        description: 'Overall strategy performance'
      },
      { 
        key: 'Sharpe Ratio', 
        value: metrics.sharpeRatio.toFixed(3),
        change: 'Risk-adjusted returns',
        icon: Activity,
        trend: metrics.sharpeRatio > 1 ? 'positive' : 'negative',
        description: 'Higher is better'
      },
      { 
        key: 'Max Drawdown', 
        value: `${(metrics.maxDrawdown * 100).toFixed(2)}%`,
        change: 'Worst peak-to-trough decline',
        icon: TrendingDown,
        trend: metrics.maxDrawdown < 0.1 ? 'positive' : 'negative',
        description: 'Lower is better'
      },
      { 
        key: 'Win Rate', 
        value: `${(metrics.winRate * 100).toFixed(2)}%`,
        change: 'Successful trade percentage',
        icon: Target,
        trend: metrics.winRate > 0.5 ? 'positive' : 'negative',
        description: 'Trade success frequency'
      },
      { 
        key: 'Volatility', 
        value: `${(metrics.volatility * 100).toFixed(2)}%`,
        change: 'Portfolio risk measure',
        icon: BarChart3,
        trend: metrics.volatility < 0.15 ? 'positive' : 'negative',
        description: 'Annualized standard deviation'
      },
      { 
        key: 'Profit Factor', 
        value: metrics.profitFactor.toFixed(2),
        change: 'Gross profit vs gross loss',
        icon: DollarSign,
        trend: metrics.profitFactor > 1.5 ? 'positive' : 'negative',
        description: 'Higher is better'
      }
    ];
  };

  const getRecentTrades = () => {
    if (!backtestResults?.trades) return [];
    return backtestResults.trades.slice(0, 5); // Last 5 trades
  };

  return (
    <div className="page-content">
      <div className="page-header">
        <h1 className="page-title">Backtest Studio</h1>
        <p className="page-subtitle">Test and optimize your trading strategies with advanced analytics</p>
      </div>

      <div className="studio-layout">
        {/* Configuration Panel */}
        <div className="config-panel">
          <div className="panel-header">
            <h3 className="panel-title">
              <Calendar className="panel-icon" />
              Strategy Configuration
            </h3>
            <p className="panel-subtitle">Configure your backtest parameters</p>
          </div>
          
          <div className="config-form">
            <div className="form-section">
              <label className="form-label">Initial Capital ($)</label>
              <input
                type="number"
                value={config.initialCapital}
                onChange={(e) => setConfig({...config, initialCapital: Number(e.target.value)})}
                className="form-input"
                min="1000"
                step="1000"
              />
            </div>

            <div className="form-grid">
              <div className="form-section">
                <label className="form-label">Start Date</label>
                <input
                  type="date"
                  value={config.startDate}
                  onChange={(e) => setConfig({...config, startDate: e.target.value})}
                  className="form-input"
                />
              </div>
              <div className="form-section">
                <label className="form-label">End Date</label>
                <input
                  type="date"
                  value={config.endDate}
                  onChange={(e) => setConfig({...config, endDate: e.target.value})}
                  className="form-input"
                />
              </div>
            </div>

            <div className="form-section">
              <label className="form-label">Rebalance Frequency</label>
              <select
                value={config.rebalanceFrequency}
                onChange={(e) => setConfig({...config, rebalanceFrequency: e.target.value})}
                className="form-input"
              >
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="quarterly">Quarterly</option>
              </select>
            </div>

            <div className="form-section">
              <label className="form-label">Trading Strategy</label>
              <select
                value={config.strategy}
                onChange={(e) => setConfig({...config, strategy: e.target.value})}
                className="form-input"
              >
                <option value="momentum">Momentum</option>
                <option value="mean-reversion">Mean Reversion</option>
                <option value="value">Value Investing</option>
                <option value="growth">Growth Investing</option>
                <option value="sector-rotation">Sector Rotation</option>
              </select>
            </div>

            <div className="form-section">
              <label className="form-label">Tickers (comma separated)</label>
              <input
                type="text"
                value={config.symbols.join(', ')}
                onChange={(e) => setConfig({...config, symbols: e.target.value.split(',').map(s => s.trim())})}
                className="form-input"
                placeholder="AAPL, MSFT, GOOGL, AMZN"
              />
            </div>

            <button
              onClick={handleRunBacktest}
              disabled={loading}
              className="btn btn-primary run-btn"
            >
              <Play className="btn-icon" />
              <span>{loading ? 'Running Analysis...' : 'Run Backtest'}</span>
              {loading && <div className="btn-spinner"></div>}
            </button>
          </div>
        </div>

        {/* Results Panel */}
        <div className="results-panel">
          <div className="panel-header">
            <h3 className="panel-title">Backtest Results</h3>
            <p className="panel-subtitle">
              {backtestResults ? 'Strategy performance analysis' : 'Configure and run backtest to see results'}
            </p>
          </div>
          
          {loading ? (
            <div className="loading-state">
              <div className="quant-spinner"></div>
              <h4>Running Backtest Analysis</h4>
              <p>Simulating trades and calculating performance metrics...</p>
              <div className="pulse-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          ) : backtestResults ? (
            <div className="results-content">
              {/* Key Metrics */}
              <div className="metrics-section">
                <h4 className="section-title">Performance Metrics</h4>
                <div className="metrics-grid">
                  {getMetrics().map((metric) => {
                    const Icon = metric.icon;
                    return (
                      <div key={metric.key} className="metric-card">
                        <div className="metric-header">
                          <div className={`metric-icon-container ${metric.trend}`}>
                            <Icon className="metric-icon" size={20} />
                          </div>
                          <span className={`metric-trend trend-${metric.trend}`}>
                            {metric.change}
                          </span>
                        </div>
                        <div className="metric-content">
                          <h3>{metric.key}</h3>
                          <div className="metric-value">{metric.value}</div>
                          <p className="metric-description">{metric.description}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Performance Chart */}
              <div className="chart-section">
                <h4 className="section-title">Portfolio Performance</h4>
                <div className="chart-container">
                  <PerformanceChart 
                    portfolioData={backtestResults.portfolioHistory}
                    benchmarkData={backtestResults.benchmarkHistory}
                    height={400}
                  />
                </div>
              </div>

              {/* Additional Metrics & Trades */}
              <div className="additional-grid">
                <div className="trades-section">
                  <h4 className="section-title">Recent Trades</h4>
                  <div className="trades-list">
                    {getRecentTrades().map((trade, index) => (
                      <div key={index} className="trade-item">
                        <div className="trade-symbol">{trade.symbol}</div>
                        <div className={`trade-side ${trade.side.toLowerCase()}`}>
                          {trade.side}
                        </div>
                        <div className="trade-quantity">{trade.quantity} shares</div>
                        <div className="trade-price">${trade.price.toFixed(2)}</div>
                        <div className={`trade-pnl ${trade.pnl >= 0 ? 'positive' : 'negative'}`}>
                          {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="stats-section">
                  <h4 className="section-title">Strategy Statistics</h4>
                  <div className="stats-grid">
                    <div className="stat-item">
                      <span className="stat-label">Total Trades</span>
                      <span className="stat-value">{backtestResults.trades.length}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Win Rate</span>
                      <span className="stat-value positive">
                        {(backtestResults.metrics.winRate * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Avg. Trade Duration</span>
                      <span className="stat-value">5.2 days</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Largest Gain</span>
                      <span className="stat-value positive">+12.4%</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Largest Loss</span>
                      <span className="stat-value negative">-8.7%</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Profit Factor</span>
                      <span className="stat-value">
                        {backtestResults.metrics.profitFactor.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <Play className="empty-icon" size={64} />
              <h4>No Backtest Results</h4>
              <p>Configure your strategy parameters and run a backtest to see performance analytics</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Mock data generators
function generateMockTrades(): Trade[] {
  const trades: Trade[] = [];
  const symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META'];
  
  for (let i = 0; i < 25; i++) {
    trades.push({
      symbol: symbols[Math.floor(Math.random() * symbols.length)],
      quantity: Math.floor(Math.random() * 100) + 10,
      price: Math.random() * 500 + 50,
      timestamp: `2023-${String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')}-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`,
      side: Math.random() > 0.5 ? 'BUY' : 'SELL',
      pnl: (Math.random() - 0.3) * 2000
    });
  }
  
  return trades;
}

// Replace the existing generatePortfolioHistory and generateBenchmarkHistory functions:

function generatePortfolioHistory() {
  const history = [];
  let value = 100000;
  const startDate = new Date('2020-01-01');
  
  // Create more realistic market data with trends and volatility
  let trend = 0.002; // Slight upward trend
  let volatility = 0.08;
  
  for (let i = 0; i < 48; i++) { // 4 years of monthly data
    const date = new Date(startDate);
    date.setMonth(date.getMonth() + i);
    
    // Realistic market simulation with momentum
    const randomChange = (Math.random() - 0.5) * volatility;
    const monthlyReturn = trend + randomChange;
    
    // Add some momentum effect
    if (i > 0) {
      const prevReturn = (history[i-1].value / (i > 1 ? history[i-2].value : 100000)) - 1;
      if (prevReturn > 0.02) {
        trend = 0.003; // Positive momentum
      } else if (prevReturn < -0.02) {
        trend = 0.001; // Negative momentum
      }
    }
    
    value *= (1 + monthlyReturn);
    
    // Ensure minimum value
    value = Math.max(value, 80000);
    
    history.push({
      date: date.toISOString().split('T')[0],
      value: Math.round(value)
    });
  }
  
  return history;
}

function generateBenchmarkHistory() {
  const history = [];
  let value = 100000;
  const startDate = new Date('2020-01-01');
  
  // Benchmark (SPY-like) with less volatility
  let trend = 0.0015;
  let volatility = 0.05;
  
  for (let i = 0; i < 48; i++) {
    const date = new Date(startDate);
    date.setMonth(date.getMonth() + i);
    
    const randomChange = (Math.random() - 0.5) * volatility;
    const monthlyReturn = trend + randomChange;
    
    value *= (1 + monthlyReturn);
    value = Math.max(value, 85000);
    
    history.push({
      date: date.toISOString().split('T')[0],
      value: Math.round(value)
    });
  }
  
  return history;
}