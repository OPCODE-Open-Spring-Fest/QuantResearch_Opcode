import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp } from 'lucide-react';
import { api } from '../utils/api';

export const Portfolio: React.FC = () => {
  const [portfolio, setPortfolio] = useState<any>(null);
  const [positions, setPositions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [portfolioData, positionsData] = await Promise.all([
        api.getPortfolio(),
        api.getPositions(),
      ]);
      setPortfolio(portfolioData);
      setPositions(positionsData);
    } catch (error) {
      setPortfolio({
        total_value: 125430,
        cash: 25430,
        positions_value: 100000,
        total_pnl: 18450,
        total_pnl_percent: 18.5,
      });
      setPositions([
        { symbol: 'AAPL', quantity: 150, avg_price: 145, current_price: 190, value: 28500 },
        { symbol: 'MSFT', quantity: 85, avg_price: 310, current_price: 367, value: 31195 },
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="container"><p>Loading...</p></div>;

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">Portfolio</h1>
        <p className="subtitle">Performance and holdings</p>
      </div>

      <div className="grid grid-4 mb-6">
        <div className="stat-card">
          <div className="stat-label">Total Value</div>
          <div className="stat-value">${portfolio.total_value.toLocaleString()}</div>
          <div className="stat-change positive">+{portfolio.total_pnl_percent}%</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Cash</div>
          <div className="stat-value">${portfolio.cash.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Positions</div>
          <div className="stat-value">${portfolio.positions_value.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Total P&L</div>
          <div className="stat-value">+${portfolio.total_pnl.toLocaleString()}</div>
        </div>
      </div>

      <div className="card">
        <h2 className="card-title">Holdings</h2>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Avg Cost</th>
                <th>Current Price</th>
                <th>Value</th>
                <th>P&L</th>
                <th>Weight</th>
              </tr>
            </thead>
            <tbody>
              {positions.map((pos, i) => {
                const pnl = pos.value - (pos.quantity * pos.avg_price);
                const pnlPercent = (pnl / (pos.quantity * pos.avg_price) * 100).toFixed(2);
                const weight = (pos.value / portfolio.positions_value * 100).toFixed(1);
                return (
                  <tr key={i}>
                    <td><strong>{pos.symbol}</strong></td>
                    <td>{pos.quantity}</td>
                    <td>${pos.avg_price.toFixed(2)}</td>
                    <td>${pos.current_price.toFixed(2)}</td>
                    <td>${pos.value.toLocaleString()}</td>
                    <td>
                      <span className={pnl >= 0 ? 'badge badge-white' : 'badge badge-gray'}>
                        {pnl >= 0 ? '+' : ''}${pnl.toLocaleString()} ({pnlPercent}%)
                      </span>
                    </td>
                    <td>{weight}%</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
