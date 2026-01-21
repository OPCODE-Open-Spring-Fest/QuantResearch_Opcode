# Complete Final Code - Frontend Files

## 1. API Client (`src/utils/api.ts`)

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
  };
};

// Helper to handle API errors consistently
const handleApiError = async (response: Response) => {
  if (response.status === 401) {
    // Unauthorized - clear token and redirect to login
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
    throw new Error('Session expired. Please login again.');
  }
  
  const errorData = await response.json().catch(() => ({}));
  throw new Error(errorData.detail || errorData.message || `Request failed (${response.status})`);
};

export const api = {
  // Auth
  login: async (email: string, password: string) => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      
      const response = await fetch(`${API_URL}/api/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Login failed (${response.status})`);
      }
      
      return response.json();
    } catch (error: any) {
      if (error.message.includes('fetch')) {
        throw new Error('Cannot connect to backend. Is the server running on port 8000?');
      }
      throw error;
    }
  },

  register: async (email: string, password: string) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password }),
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Registration failed (${response.status})`);
      }
      
      return response.json();
    } catch (error: any) {
      if (error.message.includes('fetch')) {
        throw new Error('Cannot connect to backend. Is the server running on port 8000?');
      }
      throw error;
    }
  },

  getCurrentUser: async () => {
    const response = await fetch(`${API_URL}/api/auth/me`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  // Dashboard
  getDashboardStats: async () => {
    const response = await fetch(`${API_URL}/api/dashboard/overview`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  getDashboardPositions: async () => {
    const response = await fetch(`${API_URL}/api/dashboard/positions`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  getDashboardTrades: async () => {
    const response = await fetch(`${API_URL}/api/dashboard/trades`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  getStockQuote: async (symbol: string) => {
    const response = await fetch(`${API_URL}/api/stocks/quote/${symbol}`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  // Trading
  buyStock: async (data: { symbol: string; quantity: number; price: number }) => {
    const response = await fetch(`${API_URL}/api/positions/buy`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  sellStock: async (data: { symbol: string; quantity: number; price: number }) => {
    const response = await fetch(`${API_URL}/api/positions/sell`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  getPositions: async () => {
    const response = await fetch(`${API_URL}/api/positions`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  getTrades: async () => {
    const response = await fetch(`${API_URL}/api/trades`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  // Portfolio
  getPortfolio: async () => {
    const response = await fetch(`${API_URL}/api/portfolio/balance`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  depositCash: async (amount: number) => {
    const response = await fetch(`${API_URL}/api/portfolio/deposit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ amount }),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  withdrawCash: async (amount: number) => {
    const response = await fetch(`${API_URL}/api/portfolio/withdraw`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ amount }),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  // Backtest
  runBacktest: async (config: any) => {
    const response = await fetch(`${API_URL}/api/backtest`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(config),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  getBacktestResults: async (jobId: string) => {
    const response = await fetch(`${API_URL}/api/backtest/${jobId}/results`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  // Watchlists
  getWatchlists: async () => {
    const response = await fetch(`${API_URL}/api/watchlists`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  createWatchlist: async (name: string) => {
    const response = await fetch(`${API_URL}/api/watchlists`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ name }),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  addToWatchlist: async (id: number, symbol: string) => {
    const response = await fetch(`${API_URL}/api/watchlists/${id}/symbols`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ symbol }),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  // Alerts
  getAlerts: async () => {
    const response = await fetch(`${API_URL}/api/alerts`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  createAlert: async (data: { symbol: string; price: number; condition: string }) => {
    const response = await fetch(`${API_URL}/api/alerts`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  deleteAlert: async (id: number) => {
    const response = await fetch(`${API_URL}/api/alerts/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  // Strategies
  getStrategies: async () => {
    const response = await fetch(`${API_URL}/api/strategies`, {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  createStrategy: async (data: any) => {
    const response = await fetch(`${API_URL}/api/strategies`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  activateStrategy: async (id: number) => {
    const response = await fetch(`${API_URL}/api/strategies/${id}/activate`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },

  deactivateStrategy: async (id: number) => {
    const response = await fetch(`${API_URL}/api/strategies/${id}/deactivate`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      await handleApiError(response);
    }
    return response.json();
  },
};
```

## 2. Auth Context (`src/context/AuthContext.tsx`)

```typescript
import React, { createContext, useContext, useEffect, useState } from 'react';

type User = {
  id: number;
  username: string;
  email: string;
};

type AuthContextValue = {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuthData: (token: string, user: User) => void;
  clearAuth: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Load auth data from localStorage on mount
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setToken(storedToken);
        setUser(parsedUser);
      } catch (err) {
        // Clear invalid data
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const setAuthData = (newToken: string, newUser: User) => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem('token', newToken);
    localStorage.setItem('user', JSON.stringify(newUser));
  };

  const clearAuth = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider 
      value={{ 
        user, 
        token, 
        isAuthenticated: !!token,
        setAuthData,
        clearAuth
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}
```

## 3. Main Entry (`src/main.tsx`)

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './AppNew';
import { AuthProvider } from './context/AuthContext';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
```

## 4. Environment Configuration (`.env`)

```env
# Backend API URL (must match where backend is running)
VITE_API_URL=http://localhost:8000

# WebSocket URL (for real-time updates)
VITE_WS_URL=ws://localhost:8000
```

## 5. App Router (`src/AppNew.tsx`)

```typescript
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { Trading } from './pages/Trading';
import { Portfolio } from './pages/Portfolio';
import { Backtest } from './pages/Backtest';
import { Cash } from './pages/Cash';
import { Watchlists } from './pages/Watchlists';
import { Alerts } from './pages/Alerts';
import { SystemStatus } from './pages/SystemStatus';
import { Auth } from './pages/Auth';
import './App.css';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = localStorage.getItem('token');
  const location = useLocation();
  
  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Auth />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <div className="app">
                <Sidebar />
                <div className="main">
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/trading" element={<Trading />} />
                    <Route path="/portfolio" element={<Portfolio />} />
                    <Route path="/backtest" element={<Backtest />} />
                    <Route path="/cash" element={<Cash />} />
                    <Route path="/watchlists" element={<Watchlists />} />
                    <Route path="/alerts" element={<Alerts />} />
                    <Route path="/status" element={<SystemStatus />} />
                  </Routes>
                </div>
              </div>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};
```

## Quick Start Commands

### Start Backend
```bash
cd c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch
uvicorn src.quant_research_starter.api.main:app --reload --port 8000
```

### Start Frontend
```bash
cd src\quant_research_starter\frontend\cauweb
npm run dev
```

### Access Application
- Frontend: http://localhost:3003
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Testing

1. Open http://localhost:3003
2. Register a new account
3. Login with your credentials
4. Navigate through the dashboard
5. Try trading, portfolio, and backtest features

## Key Features

✅ JWT-based authentication  
✅ Protected routes with auto-redirect  
✅ Centralized API client  
✅ Automatic token management  
✅ Session expiry handling  
✅ Error handling with user feedback  
✅ Environment-based configuration  
✅ CORS properly configured  
✅ TypeScript type safety  

---

**Status**: Production Ready ✅
