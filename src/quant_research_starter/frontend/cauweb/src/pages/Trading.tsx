import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, RefreshCw } from 'lucide-react';
import { api } from '../utils/api';
import { useToast } from '../hooks/useToast';
import { ToastContainer } from '../components/Toast';

export const Trading: React.FC = () => {
  const [symbol, setSymbol] = useState('');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [positions, setPositions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const { toasts, removeToast, success, error } = useToast();

  useEffect(() => {
    loadPositions();
  }, []);

  const loadPositions = async () => {
    setRefreshing(true);
    try {
      const data = await api.getPositions();
      setPositions(data);
      success('Positions loaded successfully');
    } catch (err) {
      error('Failed to load positions');
      setPositions([
        { symbol: 'AAPL', quantity: 150, avg_price: 145, current_price: 190, pnl: 6750 },
        { symbol: 'MSFT', quantity: 85, avg_price: 310, current_price: 367, pnl: 4845 },
        { symbol: 'GOOGL', quantity: 50, avg_price: 2800, current_price: 2950, pnl: 7500 },
      ]);
    } finally {
      setRefreshing(false);
    }
  };

  const handleBuy = async () => {
    if (!symbol || !quantity || !price) {
      error('Please fill in all fields');
      return;
    }
    setLoading(true);
    try {
      await api.buyStock({
        symbol: symbol.toUpperCase(),
        quantity: parseInt(quantity),
        price: parseFloat(price),
      });
      success(`Bought ${quantity} shares of ${symbol.toUpperCase()}`);
      setSymbol('');
      setQuantity('');
      setPrice('');
      loadPositions();
    } catch (err: any) {
      error(err.message || 'Failed to buy stock');
    } finally {
      setLoading(false);
    }
  };

  const handleSell = async () => {
    if (!symbol || !quantity || !price) {
      error('Please fill in all fields');
      return;
    }
    setLoading(true);
    try {
      await api.sellStock({
        symbol: symbol.toUpperCase(),
        quantity: parseInt(quantity),
        price: parseFloat(price),
      });
      success(`Sold ${quantity} shares of ${symbol.toUpperCase()}`);
      setSymbol('');
      setQuantity('');
      setPrice('');
      loadPositions();
    } catch (err: any) {
      error(err.message || 'Failed to sell stock');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container fade-in">
      <ToastContainer toasts={toasts} onClose={removeToast} />
      
      <div className="header">
        <div>
          <h1 className="title">Trading</h1>
          <p className="subtitle">Buy and sell stocks in real-time</p>
        </div>
        <button 
          onClick={loadPositions} 
          className="btn btn-outline"
          disabled={refreshing}
        >
          <RefreshCw size={20} className={refreshing ? 'loading' : ''} />
          Refresh
        </button>
      </div>

      <div className="grid grid-2 mb-6">
        <div className="card">
          <h2 className="card-title">Place Order</h2>
          <div className="form-group">
            <label className="label">Symbol</label>
            <input
              className="input"
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              placeholder="AAPL"
            />
          </div>
          <div className="form-group">
            <label className="label">Quantity</label>
            <input
              className="input"
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              placeholder="100"
            />
          </div>
          <div className="form-group">
            <label className="label">Price</label>
            <input
              className="input"
              type="number"
              step="0.01"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              placeholder="150.00"
            />
          </div>
          <div className="flex gap-4">
            <button className="btn btn-primary" onClick={handleBuy} disabled={loading} style={{ flex: 1 }}>
              <TrendingUp size={20} />
              Buy
            </button>
            <button className="btn btn-secondary" onClick={handleSell} disabled={loading} style={{ flex: 1 }}>
              <TrendingDown size={20} />
              Sell
            </button>
          </div>
        </div>

        <div className="card">
          <h2 className="card-title">Portfolio Summary</h2>
          <div className="grid grid-2">
            <div className="stat-card">
              <div className="stat-label">Positions</div>
              <div className="stat-value">{positions.length}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Total Value</div>
              <div className="stat-value">
                ${positions.reduce((sum, p) => sum + p.quantity * (p.current_price || p.avg_price), 0).toLocaleString()}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="card-title" style={{ marginBottom: 0 }}>Current Positions</h2>
          <span className="badge badge-white">{positions.length} Active</span>
        </div>
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Avg Price</th>
                <th>Current Price</th>
                <th>Value</th>
                <th>P&L</th>
                <th>P&L %</th>
              </tr>
            </thead>
            <tbody>
              {positions.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '2rem', color: 'var(--gray-light)' }}>
                    No positions yet. Start trading to see your portfolio here.
                  </td>
                </tr>
              ) : (
                positions.map((pos, i) => {
                  const currentPrice = pos.current_price || pos.avg_price;
                  const pnlValue = pos.pnl || (currentPrice - pos.avg_price) * pos.quantity;
                  const pnlPercent = ((currentPrice - pos.avg_price) / pos.avg_price * 100);
                  const isProfit = pnlPercent >= 0;
                  
                  return (
                    <tr key={i}>
                      <td>
                        <strong style={{ fontSize: '1.1rem' }}>{pos.symbol}</strong>
                      </td>
                      <td>{pos.quantity.toLocaleString()}</td>
                      <td>${pos.avg_price.toFixed(2)}</td>
                      <td>
                        <strong>${currentPrice.toFixed(2)}</strong>
                      </td>
                      <td>
                        <strong>${(pos.quantity * currentPrice).toLocaleString()}</strong>
                      </td>
                      <td style={{ color: isProfit ? 'var(--white)' : 'var(--gray-light)' }}>
                        <strong>{isProfit ? '+' : ''}${pnlValue.toFixed(2)}</strong>
                      </td>
                      <td>
                        <span className={isProfit ? 'badge badge-white' : 'badge badge-gray'}>
                          {isProfit ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                          {' '}{isProfit ? '+' : ''}{pnlPercent.toFixed(2)}%
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
