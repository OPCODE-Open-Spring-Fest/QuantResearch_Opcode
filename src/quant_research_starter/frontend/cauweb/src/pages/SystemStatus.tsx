import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, RefreshCw } from 'lucide-react';

export const SystemStatus: React.FC = () => {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [lastCheck, setLastCheck] = useState<Date>(new Date());

  const checkBackend = async () => {
    setBackendStatus('checking');
    try {
      const response = await fetch('http://localhost:8000/docs', { 
        method: 'GET',
        mode: 'cors',
      });
      setBackendStatus(response.ok ? 'online' : 'offline');
    } catch (error) {
      console.error('Backend check failed:', error);
      setBackendStatus('offline');
    }
    setLastCheck(new Date());
  };

  useEffect(() => {
    checkBackend();
    const interval = setInterval(checkBackend, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container fade-in">
      <div className="header">
        <h1 className="title">System Status</h1>
        <p className="subtitle">Check backend connectivity</p>
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="card-title" style={{ marginBottom: 0 }}>Backend API</h2>
          <button onClick={checkBackend} className="btn btn-outline">
            <RefreshCw size={20} className={backendStatus === 'checking' ? 'loading' : ''} />
            Refresh
          </button>
        </div>

        <div className="flex items-center gap-4 mb-4">
          {backendStatus === 'online' && (
            <>
              <CheckCircle size={48} style={{ color: 'var(--success)' }} />
              <div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Backend Online</div>
                <div style={{ color: 'var(--gray-light)' }}>http://localhost:8000</div>
              </div>
            </>
          )}
          {backendStatus === 'offline' && (
            <>
              <XCircle size={48} style={{ color: 'var(--error)' }} />
              <div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Backend Offline</div>
                <div style={{ color: 'var(--gray-light)' }}>Cannot connect to http://localhost:8000</div>
              </div>
            </>
          )}
          {backendStatus === 'checking' && (
            <>
              <div className="spinner"></div>
              <div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Checking...</div>
                <div style={{ color: 'var(--gray-light)' }}>Connecting to backend</div>
              </div>
            </>
          )}
        </div>

        <div style={{ padding: '1rem', background: 'var(--black)', borderRadius: '6px', border: '1px solid var(--border)' }}>
          <div style={{ fontFamily: 'monospace', fontSize: '0.875rem' }}>
            <div>Frontend URL: http://localhost:3006</div>
            <div>Backend URL: http://localhost:8000</div>
            <div>Last Check: {lastCheck.toLocaleTimeString()}</div>
            <div>Status: {backendStatus}</div>
          </div>
        </div>

        {backendStatus === 'offline' && (
          <div className="alert" style={{ marginTop: '1.5rem' }}>
            <strong>Troubleshooting:</strong>
            <ul style={{ marginLeft: '1.5rem', marginTop: '0.5rem' }}>
              <li>Make sure backend is running: <code style={{ background: 'var(--gray-mid)', padding: '2px 6px', borderRadius: '3px' }}>uvicorn src.quant_research_starter.api.main:app --reload --port 8000</code></li>
              <li>Check if port 8000 is not blocked by firewall</li>
              <li>Verify CORS settings in backend main.py</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};
