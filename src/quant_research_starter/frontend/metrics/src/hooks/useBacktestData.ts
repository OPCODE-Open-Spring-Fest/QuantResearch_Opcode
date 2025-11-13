import { useState, useEffect } from 'react';
import { BacktestData } from '../types';

// Mock data generator - replace with actual API calls
const generateMockData = (): BacktestData => {
  const baseValue = 10000;
  const performance: any[] = [];
  const drawdown: any[] = [];
  
  let currentValue = baseValue;
  let peak = baseValue;
  
  for (let i = 0; i < 100; i++) {
    const date = new Date();
    date.setDate(date.getDate() - (99 - i));
    
    // Generate random return between -2% and +3%
    const dailyReturn = (Math.random() * 0.05) - 0.02;
    currentValue = currentValue * (1 + dailyReturn);
    peak = Math.max(peak, currentValue);
    const currentDrawdown = (currentValue - peak) / peak;
    
    performance.push({
      date: date.toISOString().split('T')[0],
      value: currentValue,
      benchmark: baseValue * (1 + (i * 0.0005)) // Simple benchmark
    });
    
    drawdown.push({
      date: date.toISOString().split('T')[0],
      drawdown: currentDrawdown
    });
  }
  
  const totalReturn = (currentValue - baseValue) / baseValue;
  
  return {
    id: '1',
    timestamp: new Date().toISOString(),
    metrics: {
      totalReturn,
      sharpeRatio: 1.2 + Math.random() * 0.8,
      maxDrawdown: Math.min(...drawdown.map(d => d.drawdown)),
      volatility: 0.15 + Math.random() * 0.1,
      winRate: 0.55 + Math.random() * 0.15,
      profitFactor: 1.5 + Math.random() * 0.8
    },
    performance,
    drawdown
  };
};

export const useBacktestData = () => {
  const [data, setData] = useState<BacktestData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Replace this with actual API call
        const mockData = generateMockData();
        setData(mockData);
        setError(null);
      } catch (err) {
        setError('Failed to load backtest data');
        console.error('Error fetching backtest data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const refreshData = async () => {
    try {
      setLoading(true);
      await new Promise(resolve => setTimeout(resolve, 800));
      const mockData = generateMockData();
      setData(mockData);
      setError(null);
    } catch (err) {
      setError('Failed to refresh data');
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refreshData };
};