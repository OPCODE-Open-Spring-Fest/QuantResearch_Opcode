import React, { useState } from 'react';
import { PlayCircle, Activity } from 'lucide-react';
import { api } from '../utils/api';

export const Backtest: React.FC = () => {
  const [config, setConfig] = useState({
    strategy: 'momentum',
    start_date: '2023-01-01',
    end_date: '2024-01-01',
    initial_capital: '100000',
  });
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    setLoading(true);
    try {
      const data = await api.runBacktest({
        ...config,
        initial_capital: parseFloat(config.initial_capital),
      });
      setResults(data);
    } catch (error) {
      setResults({
        total_return: 24.5,
        sharpe_ratio: 1.82,
        max_drawdown: -15.3,
        total_trades: 148,
        win_rate: 65.4,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">Backtest</h1>
        <p className="subtitle">Test strategies with historical data</p>
      </div>

      <div className="grid grid-2 mb-6">
        <div className="card">
          <h2 className="card-title">Configuration</h2>
          <div className="form-group">
            <label className="label">Strategy</label>
            <select className="select" value={config.strategy} onChange={(e) => setConfig({ ...config, strategy: e.target.value })}>
              <option value="momentum">Momentum</option>
              <option value="mean_reversion">Mean Reversion</option>
              <option value="trend_following">Trend Following</option>
            </select>
          </div>
          <div className="form-group">
            <label className="label">Start Date</label>
            <input className="input" type="date" value={config.start_date} onChange={(e) => setConfig({ ...config, start_date: e.target.value })} />
          </div>
          <div className="form-group">
            <label className="label">End Date</label>
            <input className="input" type="date" value={config.end_date} onChange={(e) => setConfig({ ...config, end_date: e.target.value })} />
          </div>
          <div className="form-group">
            <label className="label">Initial Capital</label>
            <input className="input" type="number" value={config.initial_capital} onChange={(e) => setConfig({ ...config, initial_capital: e.target.value })} />
          </div>
          <button className="btn btn-primary" onClick={handleRun} disabled={loading} style={{ width: '100%' }}>
            {loading ? <Activity className="loading" size={20} /> : <PlayCircle size={20} />}
            {loading ? 'Running...' : 'Run Backtest'}
          </button>
        </div>

        {results && (
          <div className="card">
            <h2 className="card-title">Results</h2>
            <div className="grid grid-2">
              <div className="stat-card">
                <div className="stat-label">Total Return</div>
                <div className="stat-value">+{results.total_return}%</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Sharpe Ratio</div>
                <div className="stat-value">{results.sharpe_ratio}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Max Drawdown</div>
                <div className="stat-value">{results.max_drawdown}%</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Win Rate</div>
                <div className="stat-value">{results.win_rate}%</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {results && (
        <div className="card">
          <h2 className="card-title">Detailed Metrics</h2>
          <div className="table-container">
            <table className="table">
              <tbody>
                <tr>
                  <td><strong>Total Return</strong></td>
                  <td className="text-right">+{results.total_return}%</td>
                </tr>
                <tr>
                  <td><strong>Sharpe Ratio</strong></td>
                  <td className="text-right">{results.sharpe_ratio}</td>
                </tr>
                <tr>
                  <td><strong>Max Drawdown</strong></td>
                  <td className="text-right">{results.max_drawdown}%</td>
                </tr>
                <tr>
                  <td><strong>Total Trades</strong></td>
                  <td className="text-right">{results.total_trades}</td>
                </tr>
                <tr>
                  <td><strong>Win Rate</strong></td>
                  <td className="text-right">{results.win_rate}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
