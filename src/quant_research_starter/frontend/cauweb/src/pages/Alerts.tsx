import React, { useState, useEffect } from 'react';
import { Bell, Plus, Trash2, TrendingUp, TrendingDown } from 'lucide-react';
import { api } from '../utils/api';
import { useToast } from '../hooks/useToast';
import { ToastContainer } from '../components/Toast';

export const Alerts: React.FC = () => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [symbol, setSymbol] = useState('');
  const [condition, setCondition] = useState('above');
  const [price, setPrice] = useState('');
  const [loading, setLoading] = useState(false);
  const { toasts, removeToast, success, error } = useToast();

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      const data = await api.getAlerts();
      setAlerts(data);
      success('Alerts loaded successfully');
    } catch (err) {
      error('Failed to load alerts');
      setAlerts([
        { id: 1, symbol: 'AAPL', condition: 'above', price: 200, active: true },
        { id: 2, symbol: 'MSFT', condition: 'below', price: 350, active: true },
        { id: 3, symbol: 'GOOGL', condition: 'above', price: 3000, active: false },
      ]);
    }
  };

  const handleCreate = async () => {
    if (!symbol || !price) {
      error('Please fill in all fields');
      return;
    }
    setLoading(true);
    try {
      await api.createAlert({
        symbol: symbol.toUpperCase(),
        condition,
        price: parseFloat(price),
      });
      success(`Alert created for ${symbol.toUpperCase()}`);
      setSymbol('');
      setPrice('');
      loadAlerts();
    } catch (err: any) {
      error(err.message || 'Failed to create alert');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.deleteAlert(id);
      success('Alert deleted');
      loadAlerts();
    } catch (err: any) {
      error(err.message || 'Failed to delete alert');
    }
  };

  return (
    <div className="container fade-in">
      <ToastContainer toasts={toasts} onClose={removeToast} />
      
      <div className="header">
        <div>
          <h1 className="title">Price Alerts</h1>
          <p className="subtitle">Get notified when stocks hit your target price</p>
        </div>
      </div>

      <div className="grid grid-3 mb-6">
        <div className="stat-card">
          <Bell size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Active Alerts</div>
          <div className="stat-value">{alerts.filter(a => a.active).length}</div>
        </div>

        <div className="stat-card">
          <TrendingUp size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Above Price</div>
          <div className="stat-value">{alerts.filter(a => a.condition === 'above').length}</div>
        </div>

        <div className="stat-card">
          <TrendingDown size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Below Price</div>
          <div className="stat-value">{alerts.filter(a => a.condition === 'below').length}</div>
        </div>
      </div>

      <div className="card mb-6">
        <h2 className="card-title">Create Alert</h2>
        <div className="grid grid-3 gap-4">
          <div className="form-group">
            <label className="label">Symbol</label>
            <input
              className="input"
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="AAPL"
            />
          </div>
          <div className="form-group">
            <label className="label">Condition</label>
            <select
              className="select"
              value={condition}
              onChange={(e) => setCondition(e.target.value)}
            >
              <option value="above">Above</option>
              <option value="below">Below</option>
            </select>
          </div>
          <div className="form-group">
            <label className="label">Target Price</label>
            <input
              className="input"
              type="number"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              placeholder="150.00"
            />
          </div>
        </div>
        <button className="btn btn-primary" onClick={handleCreate} disabled={loading}>
          <Plus size={20} />
          Create Alert
        </button>
      </div>

      <div className="card">
        <h2 className="card-title">Your Alerts</h2>
        {alerts.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--gray-light)' }}>
            <Bell size={48} style={{ marginBottom: '1rem', opacity: 0.3 }} />
            <p>No alerts yet. Create your first alert above.</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Condition</th>
                  <th>Target Price</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((alert) => (
                  <tr key={alert.id}>
                    <td>
                      <strong style={{ fontSize: '1.1rem' }}>{alert.symbol}</strong>
                    </td>
                    <td>
                      <span className="flex items-center gap-4">
                        {alert.condition === 'above' ? (
                          <TrendingUp size={16} />
                        ) : (
                          <TrendingDown size={16} />
                        )}
                        {alert.condition.charAt(0).toUpperCase() + alert.condition.slice(1)}
                      </span>
                    </td>
                    <td>
                      <strong>${alert.price.toFixed(2)}</strong>
                    </td>
                    <td>
                      <span className={`badge ${alert.active ? 'badge-white' : 'badge-gray'}`}>
                        {alert.active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <button
                        onClick={() => handleDelete(alert.id)}
                        className="btn btn-secondary"
                        style={{ padding: '0.5rem 1rem' }}
                      >
                        <Trash2 size={16} />
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
