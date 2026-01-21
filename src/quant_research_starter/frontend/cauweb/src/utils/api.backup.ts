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

// Default export for compatibility
export default api;
