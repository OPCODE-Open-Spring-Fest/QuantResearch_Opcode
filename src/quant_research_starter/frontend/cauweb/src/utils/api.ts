// Mock API functions for development
export interface BacktestMetrics {
  totalReturn: number;
  annualizedReturn: number;
  volatility: number;
  sharpeRatio: number;
  maxDrawdown: number;
  winRate: number;
  turnover: number;
}

export interface BacktestResult {
  metrics: BacktestMetrics;
  portfolioSnapshots: any[];
  trades: any[];
}

const API_BASE = import.meta.env.VITE_API_URL || '';

async function getAuthHeader(): Promise<Record<string, string>> {
  try {
    const token = window.localStorage.getItem('sb:token');
    if (token) return { Authorization: `Bearer ${token}` };
  } catch (err) {
    // ignore
  }
  return {};
}

export const api = {
  async runBacktest(config: any): Promise<BacktestResult> {
    if (API_BASE) {
      const headers = await getAuthHeader();
      const resp = await fetch(`${API_BASE}/api/backtest/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...headers },
        body: JSON.stringify(config),
      });
      if (!resp.ok) throw new Error(`API error ${resp.status}`);
      return resp.json();
    }

    // Fallback: simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000));
    return {
      metrics: {
        totalReturn: 0.2345,
        annualizedReturn: 0.0876,
        volatility: 0.1567,
        sharpeRatio: 1.234,
        maxDrawdown: 0.1234,
        winRate: 0.645,
        turnover: 2.34,
      },
      portfolioSnapshots: generateDemoSnapshots(),
      trades: [],
    };
  },

  async getAssets(): Promise<any[]> {
    if (API_BASE) {
      const headers = await getAuthHeader();
      const resp = await fetch(`${API_BASE}/api/assets/`, { headers });
      if (!resp.ok) throw new Error(`API error ${resp.status}`);
      return resp.json();
    }
    return [
      { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology', marketCap: 2800000000000, price: 182.63 },
      { symbol: 'MSFT', name: 'Microsoft Corp.', sector: 'Technology', marketCap: 2750000000000, price: 370.73 },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology', marketCap: 1750000000000, price: 138.21 },
      { symbol: 'AMZN', name: 'Amazon.com Inc.', sector: 'Consumer', marketCap: 1500000000000, price: 145.18 },
      { symbol: 'TSLA', name: 'Tesla Inc.', sector: 'Consumer', marketCap: 750000000000, price: 238.83 },
    ];
  },
};

function generateDemoSnapshots() {
  const snapshots = [];
  let value = 100000;
  const startDate = new Date('2020-01-01');
  
  for (let i = 0; i < 100; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i * 7);
    value *= 1 + (Math.random() - 0.45) * 0.02;
    
    snapshots.push({
      timestamp: date.toISOString(),
      totalValue: value,
      cash: 10000,
      holdingsValue: value - 10000
    });
  }
  
  return snapshots;
}