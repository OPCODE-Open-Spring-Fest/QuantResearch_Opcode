import React, { useState, useEffect } from 'react';
import { Eye, Plus, Star, Trash2, TrendingUp } from 'lucide-react';
import { api } from '../utils/api';
import { useToast } from '../hooks/useToast';
import { ToastContainer } from '../components/Toast';

export const Watchlists: React.FC = () => {
  const [watchlists, setWatchlists] = useState<any[]>([]);
  const [selectedList, setSelectedList] = useState<any>(null);
  const [name, setName] = useState('');
  const [symbol, setSymbol] = useState('');
  const [loading, setLoading] = useState(false);
  const { toasts, removeToast, success, error } = useToast();

  useEffect(() => {
    loadWatchlists();
  }, []);

  const loadWatchlists = async () => {
    try {
      const data = await api.getWatchlists();
      setWatchlists(data);
      if (data.length > 0) setSelectedList(data[0]);
      success('Watchlists loaded');
    } catch (err) {
      error('Failed to load watchlists');
      const demo = [
        {
          id: 1,
          name: 'Tech Stocks',
          symbols: [
            { symbol: 'AAPL', price: 190, change: 2.5 },
            { symbol: 'MSFT', price: 367, change: 1.8 },
            { symbol: 'GOOGL', price: 2950, change: -0.5 },
          ],
        },
        {
          id: 2,
          name: 'Growth Picks',
          symbols: [
            { symbol: 'TSLA', price: 245, change: 3.2 },
            { symbol: 'NVDA', price: 890, change: 4.5 },
          ],
        },
      ];
      setWatchlists(demo);
      setSelectedList(demo[0]);
    }
  };

  const handleCreateList = async () => {
    if (!name) {
      error('Please enter a name');
      return;
    }
    setLoading(true);
    try {
      await api.createWatchlist({ name });
      success(`Watchlist "${name}" created`);
      setName('');
      loadWatchlists();
    } catch (err: any) {
      error(err.message || 'Failed to create watchlist');
    } finally {
      setLoading(false);
    }
  };

  const handleAddSymbol = async () => {
    if (!symbol || !selectedList) {
      error('Please select a watchlist and enter a symbol');
      return;
    }
    try {
      await api.addToWatchlist(selectedList.id, { symbol: symbol.toUpperCase() });
      success(`${symbol.toUpperCase()} added to ${selectedList.name}`);
      setSymbol('');
      loadWatchlists();
    } catch (err: any) {
      error(err.message || 'Failed to add symbol');
    }
  };

  return (
    <div className="container fade-in">
      <ToastContainer toasts={toasts} onClose={removeToast} />
      
      <div className="header">
        <div>
          <h1 className="title">Watchlists</h1>
          <p className="subtitle">Track your favorite stocks</p>
        </div>
      </div>

      <div className="grid grid-3 mb-6">
        <div className="stat-card">
          <Eye size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Total Lists</div>
          <div className="stat-value">{watchlists.length}</div>
        </div>

        <div className="stat-card">
          <Star size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Tracked Symbols</div>
          <div className="stat-value">
            {watchlists.reduce((sum, w) => sum + (w.symbols?.length || 0), 0)}
          </div>
        </div>

        <div className="stat-card">
          <TrendingUp size={24} style={{ marginBottom: '0.5rem', color: 'var(--white)' }} />
          <div className="stat-label">Avg Daily Change</div>
          <div className="stat-value positive">+2.1%</div>
        </div>
      </div>

      <div className="grid grid-2 mb-6">
        <div className="card">
          <h2 className="card-title">Create Watchlist</h2>
          <div className="form-group">
            <label className="label">Name</label>
            <input
              className="input"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="My Watchlist"
            />
          </div>
          <button className="btn btn-primary" onClick={handleCreateList} disabled={loading}>
            <Plus size={20} />
            Create List
          </button>
        </div>

        <div className="card">
          <h2 className="card-title">Add Symbol</h2>
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
          <button className="btn btn-secondary" onClick={handleAddSymbol} disabled={!selectedList}>
            <Plus size={20} />
            Add to {selectedList?.name || 'Watchlist'}
          </button>
        </div>
      </div>

      <div className="card">
        <h2 className="card-title">Your Watchlists</h2>
        {watchlists.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--gray-light)' }}>
            <Eye size={48} style={{ marginBottom: '1rem', opacity: 0.3 }} />
            <p>No watchlists yet. Create your first watchlist above.</p>
          </div>
        ) : (
          <div>
            <div className="flex gap-4 mb-4" style={{ borderBottom: '1px solid var(--border)', paddingBottom: '1rem' }}>
              {watchlists.map((list) => (
                <button
                  key={list.id}
                  onClick={() => setSelectedList(list)}
                  className={`btn ${selectedList?.id === list.id ? 'btn-primary' : 'btn-outline'}`}
                >
                  <Star size={16} />
                  {list.name}
                  <span className="badge badge-gray" style={{ marginLeft: '0.5rem' }}>
                    {list.symbols?.length || 0}
                  </span>
                </button>
              ))}
            </div>

            {selectedList && (
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Symbol</th>
                      <th>Price</th>
                      <th>Change</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedList.symbols?.map((stock: any, i: number) => (
                      <tr key={i}>
                        <td>
                          <strong style={{ fontSize: '1.1rem' }}>{stock.symbol}</strong>
                        </td>
                        <td>
                          <strong>${stock.price?.toFixed(2) || '0.00'}</strong>
                        </td>
                        <td>
                          <span className={`badge ${stock.change >= 0 ? 'badge-white' : 'badge-gray'}`}>
                            {stock.change >= 0 ? '+' : ''}{stock.change?.toFixed(2) || '0.00'}%
                          </span>
                        </td>
                        <td>
                          <button className="btn btn-secondary" style={{ padding: '0.5rem 1rem' }}>
                            <Trash2 size={16} />
                            Remove
                          </button>
                        </td>
                      </tr>
                    )) || (
                      <tr>
                        <td colSpan={4} style={{ textAlign: 'center', padding: '2rem', color: 'var(--gray-light)' }}>
                          No symbols in this watchlist. Add some above.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
