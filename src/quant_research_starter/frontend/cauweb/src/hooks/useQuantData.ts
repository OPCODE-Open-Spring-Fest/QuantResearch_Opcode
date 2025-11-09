import { useState, useEffect } from 'react';

export const useQuantData = () => {
  const [assets, setAssets] = useState<any[]>([]);

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    // Mock data
    const mockAssets = [
      { symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology', marketCap: 2800000000000, price: 182.63 },
      { symbol: 'MSFT', name: 'Microsoft Corp.', sector: 'Technology', marketCap: 2750000000000, price: 370.73 },
      { symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology', marketCap: 1750000000000, price: 138.21 },
    ];
    setAssets(mockAssets);
  };

  return {
    assets,
    loading: false,
    backtestResults: null,
    runBacktest: async () => {} // Empty function for now
  };
};