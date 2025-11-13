export interface BacktestData {
  id: string;
  timestamp: string;
  metrics: {
    totalReturn: number;
    sharpeRatio: number;
    maxDrawdown: number;
    volatility: number;
    winRate: number;
    profitFactor: number;
  };
  performance: PerformanceDataPoint[];
  drawdown: DrawdownDataPoint[];
}

export interface PerformanceDataPoint {
  date: string;
  value: number;
  benchmark?: number;
}

export interface DrawdownDataPoint {
  date: string;
  drawdown: number;
}

export interface MetricCardProps {
  title: string;
  value: number | string;
  change?: number;
  format?: 'percentage' | 'currency' | 'number' | 'ratio';
  description?: string;
}

export interface ChartProps {
  data: PerformanceDataPoint[] | DrawdownDataPoint[];
  height?: number;
  loading?: boolean;
}