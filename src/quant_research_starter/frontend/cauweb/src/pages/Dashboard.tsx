import React, { useState, useEffect } from 'react';
import { TrendingUp, Activity, PlayCircle, BarChart3, DollarSign, TrendingDown } from 'lucide-react';
import { api } from '../utils/api';
import { useToast } from '../hooks/useToast';
import { ToastContainer } from '../components/Toast';

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const { toasts, removeToast, error, success } = useToast();

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await api.getDashboardStats();
      setStats(data);
      success('Dashboard loaded successfully');
    } catch (err: any) {
      error('Failed to load dashboard data');
      // Demo data fallback
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      setStats({
        total_value: 125430,
        cash_balance: 25430,
        total_return: 18.5,
        sharpe_ratio: 1.45,
        active_positions: 12,
        daily_change: 2.3,
        user_email: user.email,
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', padding: '4rem' }}>
          <div className="spinner"></div>
          <p style={{ marginTop: '1rem', color: 'var(--gray-light)' }}>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container fade-in">
      <ToastContainer toasts={toasts} onClose={removeToast} />
      
      <div className="header">
        <h1 className="title">Dashboard</h1>
        <p className="subtitle">Welcome back, {stats.user_email || 'Trader'}</p>
      </div>

      <div className="grid grid-4 mb-6">
        <div className="stat-card">
          <DollarSign size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Portfolio Value</div>
          <div className="stat-value">${stats.total_value.toLocaleString()}</div>
          <div className="stat-change positive">
            <TrendingUp size={16} /> +{stats.total_return}%
          </div>
        </div>

        <div className="stat-card">
          <Activity size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Cash Balance</div>
          <div className="stat-value">${stats.cash_balance.toLocaleString()}</div>
          <div className="stat-change">Available Funds</div>
        </div>

        <div className="stat-card">
          <TrendingUp size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Total Return</div>
          <div className="stat-value">{stats.total_return}%</div>
          <div className="stat-change positive">All Time High</div>
        </div>

        <div className="stat-card">
          <BarChart3 size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Sharpe Ratio</div>
          <div className="stat-value">{stats.sharpe_ratio}</div>
          <div className="stat-change">Risk-Adjusted</div>
        </div>
      </div>

      <div className="grid grid-3 mb-6">
        <div className="stat-card">
          <div className="stat-label">Active Positions</div>
          <div className="stat-value">{stats.active_positions || 12}</div>
          <div className="stat-change">Open Trades</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Daily Change</div>
          <div className="stat-value positive">+{stats.daily_change || 2.3}%</div>
          <div className="stat-change">
            <TrendingUp size={16} /> Today
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Win Rate</div>
          <div className="stat-value">68.5%</div>
          <div className="stat-change">Last 30 Days</div>
        </div>
      </div>

      <div className="card">
        <h2 className="card-title">Quick Actions</h2>
        <div className="flex gap-4">
          <a href="/trading" className="btn btn-primary">
            <TrendingUp size={20} />
            Start Trading
          </a>
          <a href="/backtest" className="btn btn-secondary">
            <PlayCircle size={20} />
            Run Backtest
          </a>
          <a href="/portfolio" className="btn btn-outline">
            <BarChart3 size={20} />
            View Portfolio
          </a>
        </div>
      </div>
    </div>
  );
};
