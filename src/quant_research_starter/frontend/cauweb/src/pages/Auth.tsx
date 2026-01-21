import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogIn, UserPlus, Loader } from 'lucide-react';
import { api } from '../utils/api';

export const Auth: React.FC = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Redirect to dashboard if already logged in
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/', { replace: true });
    }
  }, [navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    setLoading(true);
    
    console.log('🔥 FORM SUBMITTED!', { isLogin, email });
    
    try {
      if (isLogin) {
        console.log('Attempting login...');
        const data = await api.login(email, password);
        console.log('Login response:', data);
        
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify({ email, username: email }));
        setMessage('✅ Login successful! Redirecting...');
        
        // Force page reload to ensure app state updates
        setTimeout(() => {
          window.location.href = '/';
        }, 500);
      } else {
        console.log('Attempting registration...');
        await api.register(email, password);
        console.log('Register successful');
        
        setMessage('✅ Registration successful! Please login.');
        setIsLogin(true);
        setPassword('');
      }
    } catch (error: any) {
      console.error('Auth error:', error);
      setMessage('❌ ' + (error.message || 'Authentication failed. Check if backend is running.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '500px', paddingTop: '4rem' }}>
      <div className="card">
        <h1 className="title" style={{ textAlign: 'center', marginBottom: '2rem' }}>
          {isLogin ? 'Login' : 'Register'}
        </h1>

        {message && <div className="alert">{message}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="label">Email</label>
            <input
              className="input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="user@example.com"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label className="label">Password</label>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={loading}
            />
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginBottom: '1rem' }} disabled={loading}>
            {loading ? (
              <>
                <Loader className="icon-spin" size={20} />
                {isLogin ? 'Logging in...' : 'Registering...'}
              </>
            ) : (
              <>
                {isLogin ? <LogIn size={20} /> : <UserPlus size={20} />}
                {isLogin ? 'Login' : 'Register'}
              </>
            )}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="btn btn-outline"
            style={{ width: '100%' }}
            disabled={loading}
          >
            {isLogin ? 'Need an account? Register' : 'Have an account? Login'}
          </button>
        </div>
      </div>
    </div>
  );
};
