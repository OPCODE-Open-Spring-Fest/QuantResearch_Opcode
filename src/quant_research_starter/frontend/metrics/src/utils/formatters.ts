export const formatNumber = (value: number, type: 'percentage' | 'currency' | 'number' | 'ratio' = 'number'): string => {
  switch (type) {
    case 'percentage':
      return `${(value * 100).toFixed(2)}%`;
    case 'currency':
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(value);
    case 'ratio':
      return value.toFixed(3);
    default:
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(value);
  }
};

export const formatChange = (change: number): string => {
  const sign = change >= 0 ? '+' : '';
  return `${sign}${formatNumber(change, 'percentage')}`;
};

export const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

export const getColorForValue = (value: number, type: string): string => {
  switch (type) {
    case 'return':
    case 'winRate':
    case 'profitFactor':
      return value >= 0 ? 'text-green-600' : 'text-red-600';
    case 'drawdown':
    case 'volatility':
      return value >= 0 ? 'text-red-600' : 'text-green-600';
    default:
      return 'text-gray-900';
  }
};