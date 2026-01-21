import React, { useState } from 'react';
import { DollarSign } from 'lucide-react';
import { api } from '../utils/api';

export const Cash: React.FC = () => {
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleDeposit = async () => {
    if (!amount) {
      setMessage('❌ Please enter an amount');
      return;
    }
    setLoading(true);
    setMessage('');
    console.log('💰 Attempting deposit:', amount);
    try {
      const result = await api.depositCash(parseFloat(amount));
      console.log('✅ Deposit success:', result);
      setMessage(`✅ Deposited $${amount}`);
      setAmount('');
    } catch (error: any) {
      console.error('❌ Deposit error:', error);
      setMessage(`❌ ${error.message || 'Failed to deposit'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleWithdraw = async () => {
    if (!amount) {
      setMessage('❌ Please enter an amount');
      return;
    }
    setLoading(true);
    setMessage('');
    console.log('💸 Attempting withdraw:', amount);
    try {
      const result = await api.withdrawCash(parseFloat(amount));
      console.log('✅ Withdraw success:', result);
      setMessage(`✅ Withdrew $${amount}`);
      setAmount('');
    } catch (error: any) {
      console.error('❌ Withdraw error:', error);
      setMessage(`❌ ${error.message || 'Failed to withdraw'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1 className="title">Cash Management</h1>
        <p className="subtitle">Deposit and withdraw funds</p>
      </div>

      {message && <div className="alert">{message}</div>}

      <div className="grid grid-2">
        <div className="card">
          <h2 className="card-title">Manage Funds</h2>
          <div className="form-group">
            <label className="label">Amount</label>
            <input
              className="input"
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="10000"
            />
          </div>
          <div className="flex gap-4">
            <button className="btn btn-primary" onClick={handleDeposit} disabled={loading} style={{ flex: 1 }}>
              <DollarSign size={20} />
              Deposit
            </button>
            <button className="btn btn-secondary" onClick={handleWithdraw} disabled={loading} style={{ flex: 1 }}>
              <DollarSign size={20} />
              Withdraw
            </button>
          </div>
        </div>

        <div className="card">
          <h2 className="card-title">Account Balance</h2>
          <div className="stat-card">
            <div className="stat-label">Available Cash</div>
            <div className="stat-value">$25,430</div>
            <div className="stat-change">Ready to trade</div>
          </div>
        </div>
      </div>
    </div>
  );
};
