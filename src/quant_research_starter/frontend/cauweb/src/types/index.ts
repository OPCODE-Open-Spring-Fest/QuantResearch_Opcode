export interface PortfolioMetrics {
  totalReturn: number;
  annualizedReturn: number;
  volatility: number;
  sharpeRatio: number;
  maxDrawdown: number;
  winRate: number;
  turnover: number;
}

export interface BacktestConfig {
  initialCapital: number;
  startDate: string;
  endDate: string;
  rebalanceFrequency: 'daily' | 'weekly' | 'monthly';
  symbols: string[];
}

export interface Asset {
  symbol: string;
  name: string;
  sector: string;
  marketCap: number;
  price: number;
  volume: number;
}

export interface Trade {
  symbol: string;
  quantity: number;
  price: number;
  timestamp: string;
  side: 'BUY' | 'SELL';
}