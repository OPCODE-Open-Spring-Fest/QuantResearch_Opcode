import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Save,
  Download,
  Upload,
  Settings,
  BarChart3,
  TrendingUp,
  TrendingDown,
  Clock,
  DollarSign,
  Target,
  Activity,
  Shield,
  RefreshCw,
  Plus,
  Trash2,
  Copy,
  History,
  BookOpen,
  Zap,
  Cpu,
  LineChart,
  PieChart
} from 'lucide-react';

// Chart.js components
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

// Mock hook with enhanced data
const useQuantData = () => {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [backtestResults, setBacktestResults] = useState(null);

  const runBacktest = async (config) => {
    setLoading(true);
    setProgress(0);
    
    // Simulate progress updates
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 95) {
          clearInterval(progressInterval);
          return 95;
        }
        return prev + 5;
      });
    }, 150);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    clearInterval(progressInterval);
    setProgress(100);

    // Enhanced mock results with realistic data
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const years = [2020, 2021, 2022, 2023];
    
    const equityData = [];
    let currentValue = config.initialCapital;
    
    for (let year of years) {
      for (let month of months) {
        // Realistic market simulation with trends and noise
        const monthlyReturn = (Math.random() * 0.08 - 0.02) + 0.005; // -2% to +6% with slight positive bias
        currentValue = currentValue * (1 + monthlyReturn);
        equityData.push({
          date: `${month} ${year}`,
          value: Math.round(currentValue)
        });
      }
    }

    const drawdownData = equityData.map((point, index) => {
      const peak = Math.max(...equityData.slice(0, index + 1).map(p => p.value));
      const drawdown = ((point.value - peak) / peak) * 100;
      return { date: point.date, value: drawdown };
    });

    // Generate realistic trades
    const trades = Array.from({ length: 25 }, (_, i) => {
      const symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'JNJ', 'V'];
      const action = Math.random() > 0.4 ? 'BUY' : 'SELL';
      const basePrices = {
        'AAPL': 150, 'MSFT': 300, 'GOOGL': 2800, 'AMZN': 3300, 
        'TSLA': 200, 'META': 350, 'NVDA': 800, 'JPM': 170, 'JNJ': 160, 'V': 230
      };
      
      const symbol = symbols[Math.floor(Math.random() * symbols.length)];
      const price = basePrices[symbol] * (0.9 + Math.random() * 0.2);
      
      return {
        id: i,
        symbol,
        action,
        quantity: Math.floor(Math.random() * 100) + 10,
        price: Math.round(price * 100) / 100,
        timestamp: new Date(2020 + Math.floor(i/6), (i % 12), (i % 28) + 1),
        pnl: (Math.random() - 0.3) * 5000
      };
    });

    setBacktestResults({
      metrics: {
        totalReturn: 0.2345,
        annualizedReturn: 0.156,
        volatility: 0.182,
        sharpeRatio: 1.234,
        maxDrawdown: -0.1234,
        winRate: 0.645,
        turnover: 0.89,
        alpha: 0.0234,
        beta: 1.12,
        sortinoRatio: 1.89,
        calmarRatio: 1.45,
        informationRatio: 0.78
      },
      equityCurve: equityData,
      drawdownCurve: drawdownData,
      trades: trades.sort((a, b) => b.timestamp - a.timestamp),
      performance: {
        monthlyReturns: Array.from({ length: 36 }, () => (Math.random() - 0.5) * 0.1),
        benchmarkReturns: Array.from({ length: 36 }, () => (Math.random() - 0.5) * 0.08)
      }
    });

    setTimeout(() => setProgress(0), 1000);
    setLoading(false);
  };

  return { loading, progress, runBacktest, backtestResults };
};

export const BacktestStudio = () => {
  const { loading, progress, runBacktest, backtestResults } = useQuantData();
  const [activeTab, setActiveTab] = useState('configuration');
  const [savedStrategies, setSavedStrategies] = useState([]);
  const [strategyName, setStrategyName] = useState('');
  const [newSymbol, setNewSymbol] = useState('');

  const [config, setConfig] = useState({
    strategyName: 'Momentum Strategy v1',
    initialCapital: 100000,
    startDate: '2020-01-01',
    endDate: '2023-12-31',
    rebalanceFrequency: 'monthly',
    strategyType: 'momentum',
    universe: 'large_cap',
    riskModel: 'min_variance',
    transactionCosts: 0.001,
    maxPositionSize: 0.1,
    stopLoss: 0.05,
    takeProfit: 0.15,
    symbols: ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'JNJ', 'V']
  });

  // Chart options and data
  const equityChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        ticks: {
          color: '#6B7280',
        },
      },
      y: {
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        ticks: {
          color: '#6B7280',
          callback: function(value) {
            return '$' + value.toLocaleString();
          },
        },
      },
    },
  };

  const drawdownChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        ticks: {
          color: '#6B7280',
        },
      },
      y: {
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        ticks: {
          color: '#6B7280',
          callback: function(value) {
            return value + '%';
          },
        },
      },
    },
  };

  const getEquityChartData = () => {
    if (!backtestResults?.equityCurve) return { labels: [], datasets: [] };

    return {
      labels: backtestResults.equityCurve.map(point => point.date),
      datasets: [
        {
          label: 'Portfolio Value',
          data: backtestResults.equityCurve.map(point => point.value),
          borderColor: 'rgb(34, 197, 94)',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          fill: true,
          tension: 0.4,
        },
      ],
    };
  };

  const getDrawdownChartData = () => {
    if (!backtestResults?.drawdownCurve) return { labels: [], datasets: [] };

    return {
      labels: backtestResults.drawdownCurve.map(point => point.date),
      datasets: [
        {
          label: 'Drawdown',
          data: backtestResults.drawdownCurve.map(point => point.value),
          borderColor: 'rgb(239, 68, 68)',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          fill: true,
          tension: 0.4,
        },
      ],
    };
  };

  const strategyTypes = [
    { value: 'momentum', label: 'Momentum', description: 'Follow trending assets', icon: TrendingUp },
    { value: 'mean_reversion', label: 'Mean Reversion', description: 'Bet on price normalization', icon: Activity },
    { value: 'factor', label: 'Factor Investing', description: 'Use quantitative factors', icon: Target },
    { value: 'ml', label: 'Machine Learning', description: 'AI-powered predictions', icon: Cpu }
  ];

  const universes = [
    { value: 'large_cap', label: 'Large Cap (S&P 500)' },
    { value: 'small_cap', label: 'Small Cap (Russell 2000)' },
    { value: 'technology', label: 'Technology Sector' },
    { value: 'all', label: 'All Available Assets' }
  ];

  const riskModels = [
    { value: 'min_variance', label: 'Minimum Variance' },
    { value: 'equal_weight', label: 'Equal Weight' },
    { value: 'risk_parity', label: 'Risk Parity' },
    { value: 'black_litterman', label: 'Black-Litterman' }
  ];

  const handleRunBacktest = () => {
    runBacktest(config);
    setActiveTab('results');
  };

  const handleSaveStrategy = () => {
    if (strategyName.trim()) {
      const newStrategy = {
        id: Date.now(),
        name: strategyName,
        config: { ...config },
        createdAt: new Date().toISOString()
      };
      setSavedStrategies(prev => [newStrategy, ...prev]);
      setStrategyName('');
    }
  };

  const handleLoadStrategy = (strategy) => {
    setConfig(strategy.config);
    setActiveTab('configuration');
  };

  const addSymbol = () => {
    if (newSymbol.trim()) {
      const symbol = newSymbol.trim().toUpperCase();
      if (!config.symbols.includes(symbol)) {
        setConfig({
          ...config,
          symbols: [...config.symbols, symbol]
        });
      }
      setNewSymbol('');
    }
  };

  const removeSymbol = (index) => {
    const newSymbols = config.symbols.filter((_, i) => i !== index);
    setConfig({ ...config, symbols: newSymbols });
  };

  const formatMetricValue = (value) => {
    if (typeof value === 'number') {
      if (Math.abs(value) > 10 || (value >= -1 && value <= 1 && Math.abs(value) < 0.01)) {
        return value.toFixed(3);
      }
      return (value * 100).toFixed(2) + '%';
    }
    return String(value);
  };

  const getMetrics = () => {
    if (!backtestResults?.metrics) return [];
    
    const metrics = backtestResults.metrics;
    return [
      { key: 'totalReturn', label: 'Total Return', value: metrics.totalReturn, icon: TrendingUp, trend: metrics.totalReturn >= 0 ? 'up' : 'down' },
      { key: 'annualizedReturn', label: 'Annualized Return', value: metrics.annualizedReturn, icon: DollarSign, trend: metrics.annualizedReturn >= 0 ? 'up' : 'down' },
      { key: 'volatility', label: 'Volatility', value: metrics.volatility, icon: Activity, trend: 'neutral' },
      { key: 'sharpeRatio', label: 'Sharpe Ratio', value: metrics.sharpeRatio, icon: Target, trend: metrics.sharpeRatio >= 1 ? 'up' : 'down' },
      { key: 'maxDrawdown', label: 'Max Drawdown', value: metrics.maxDrawdown, icon: TrendingDown, trend: 'down' },
      { key: 'winRate', label: 'Win Rate', value: metrics.winRate, icon: Target, trend: metrics.winRate >= 0.5 ? 'up' : 'down' },
      { key: 'alpha', label: 'Alpha', value: metrics.alpha, icon: TrendingUp, trend: metrics.alpha >= 0 ? 'up' : 'down' },
      { key: 'beta', label: 'Beta', value: metrics.beta, icon: Activity, trend: 'neutral' }
    ];
  };

  // Enhanced loading component with progress
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
          <div className="relative inline-block mb-6">
            <RefreshCw className="w-12 h-12 text-blue-600 animate-spin" />
            <Zap className="w-6 h-6 text-yellow-500 absolute -top-1 -right-1 animate-pulse" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">Running Backtest</h3>
          <p className="text-gray-600 mb-6">Analyzing strategy performance across historical data</p>
          
          <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
            <div 
              className="bg-gradient-to-r from-blue-500  h-3 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-gray-500">{progress}% Complete</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50/30 p-4 md:p-6 lg:p-8">
      {/* Header Section */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8 gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-gray-900 to-blue-800 bg-clip-text text-transparent">
            Backtest Studio
          </h1>
          <p className="text-gray-600 mt-2 flex items-center gap-2">
            <Zap className="w-4 h-4 text-yellow-500" />
            Test, optimize, and validate your trading strategies with precision
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button className="flex items-center gap-2 bg-white/80 backdrop-blur-sm border border-gray-200 hover:bg-white text-gray-700 px-4 py-2.5 rounded-xl transition-all duration-200 hover:shadow-md hover:border-gray-300">
            <History className="w-4 h-4" />
            <span className="font-medium">History</span>
          </button>
          <button className="flex items-center gap-2 bg-white/80 backdrop-blur-sm border border-gray-200 hover:bg-white text-gray-700 px-4 py-2.5 rounded-xl transition-all duration-200 hover:shadow-md hover:border-gray-300">
            <BookOpen className="w-4 h-4" />
            <span className="font-medium">Templates</span>
          </button>
          <button className="flex items-center gap-2 bg-gradient-to-r from-blue-600 hover:from-blue-700 hover:to-purple-700 text-white px-4 py-2.5 rounded-xl transition-all duration-200 hover:shadow-lg transform hover:-translate-y-0.5">
            <Download className="w-4 h-4" />
            <span className="font-medium">Export Results</span>
          </button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200/60 mb-8 bg-white/50 backdrop-blur-sm rounded-t-xl p-1">
        {[
          { id: 'configuration', label: 'Configuration', icon: Settings },
          { id: 'results', label: 'Results', icon: BarChart3 },
          { id: 'saved', label: 'Saved Strategies', icon: Save }
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium text-sm transition-all duration-200 ${
                activeTab === tab.id
                  ? 'bg-white text-blue-600 shadow-sm border border-blue-100'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-white/50'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 md:gap-8">
        {/* Configuration Panel */}
        {activeTab === 'configuration' && (
          <>
            <div className="xl:col-span-2">
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-6 md:p-8">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
                  <div>
                    <h3 className="text-xl md:text-2xl font-bold text-gray-900">
                      Strategy Configuration
                    </h3>
                    <p className="text-gray-600 mt-1">Define your trading strategy parameters</p>
                  </div>
                  <div className="flex gap-2">
                    <button className="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2.5 rounded-xl transition-colors text-sm font-medium">
                      <Copy className="w-4 h-4" />
                      Duplicate
                    </button>
                    <button className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2.5 rounded-xl transition-colors text-sm font-medium">
                      <Save className="w-4 h-4" />
                      Save
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Basic Settings */}
                  <div className="space-y-6">
                    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-4 rounded-xl border border-blue-100">
                      <h4 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                        <Settings className="w-4 h-4 text-blue-600" />
                        Basic Settings
                      </h4>
                      
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Strategy Name
                          </label>
                          <input
                            type="text"
                            value={config.strategyName}
                            onChange={(e) => setConfig({ ...config, strategyName: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                            placeholder="Enter strategy name"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Initial Capital ($)
                          </label>
                          <input
                            type="number"
                            value={config.initialCapital}
                            onChange={(e) => setConfig({ ...config, initialCapital: Number(e.target.value) })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                          />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Start Date
                            </label>
                            <input
                              type="date"
                              value={config.startDate}
                              onChange={(e) => setConfig({ ...config, startDate: e.target.value })}
                              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              End Date
                            </label>
                            <input
                              type="date"
                              value={config.endDate}
                              onChange={(e) => setConfig({ ...config, endDate: e.target.value })}
                              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                            />
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Risk Management */}
                    <div className="bg-gradient-to-br from-red-50 to-orange-50 p-4 rounded-xl border border-red-100">
                      <h4 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                        <Shield className="w-4 h-4 text-red-600" />
                        Risk Management
                      </h4>
                      
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Transaction Costs (%)
                          </label>
                          <input
                            type="number"
                            step="0.001"
                            value={config.transactionCosts}
                            onChange={(e) => setConfig({ ...config, transactionCosts: Number(e.target.value) })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Max Position Size (%)
                          </label>
                          <input
                            type="number"
                            step="0.01"
                            value={config.maxPositionSize * 100}
                            onChange={(e) => setConfig({ ...config, maxPositionSize: Number(e.target.value) / 100 })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                          />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Stop Loss (%)
                            </label>
                            <input
                              type="number"
                              step="0.01"
                              value={config.stopLoss * 100}
                              onChange={(e) => setConfig({ ...config, stopLoss: Number(e.target.value) / 100 })}
                              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Take Profit (%)
                            </label>
                            <input
                              type="number"
                              step="0.01"
                              value={config.takeProfit * 100}
                              onChange={(e) => setConfig({ ...config, takeProfit: Number(e.target.value) / 100 })}
                              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Strategy Parameters & Asset Selection */}
                  <div className="space-y-6">
                    <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-4 rounded-xl border border-purple-100">
                      <h4 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                        <Cpu className="w-4 h-4 " />
                        Strategy Parameters
                      </h4>
                      
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Strategy Type
                          </label>
                          <select
                            value={config.strategyType}
                            onChange={(e) => setConfig({ ...config, strategyType: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                          >
                            {strategyTypes.map(type => (
                              <option key={type.value} value={type.value}>
                                {type.label}
                              </option>
                            ))}
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Asset Universe
                          </label>
                          <select
                            value={config.universe}
                            onChange={(e) => setConfig({ ...config, universe: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                          >
                            {universes.map(universe => (
                              <option key={universe.value} value={universe.value}>
                                {universe.label}
                              </option>
                            ))}
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Risk Model
                          </label>
                          <select
                            value={config.riskModel}
                            onChange={(e) => setConfig({ ...config, riskModel: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                          >
                            {riskModels.map(model => (
                              <option key={model.value} value={model.value}>
                                {model.label}
                              </option>
                            ))}
                          </select>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Rebalance Frequency
                          </label>
                          <select
                            value={config.rebalanceFrequency}
                            onChange={(e) => setConfig({ ...config, rebalanceFrequency: e.target.value })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                          >
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="monthly">Monthly</option>
                            <option value="quarterly">Quarterly</option>
                          </select>
                        </div>
                      </div>
                    </div>

                    {/* Asset Selection */}
                    <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-4 rounded-xl border border-green-100">
                      <h4 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                        <PieChart className="w-4 h-4 text-green-600" />
                        Asset Selection
                      </h4>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Symbols (Tickers)
                        </label>
                        <div className="border border-gray-300 rounded-xl p-4 bg-white/60">
                          <div className="flex flex-wrap gap-2 mb-4">
                            {config.symbols.map((symbol, index) => (
                              <span
                                key={index}
                                className="inline-flex items-center gap-1 bg-blue-100 text-blue-800 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-blue-200"
                              >
                                {symbol}
                                <button
                                  onClick={() => removeSymbol(index)}
                                  className="hover:text-blue-600 transition-colors"
                                >
                                  <Trash2 className="w-3 h-3" />
                                </button>
                              </span>
                            ))}
                          </div>
                          <div className="flex gap-2">
                            <input
                              type="text"
                              value={newSymbol}
                              onChange={(e) => setNewSymbol(e.target.value)}
                              onKeyPress={(e) => e.key === 'Enter' && addSymbol()}
                              placeholder="Add symbol (e.g., AAPL)"
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                            />
                            <button 
                              onClick={addSymbol}
                              className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-lg transition-colors"
                            >
                              <Plus className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Run Button */}
                <div className="mt-8 pt-8 border-t border-gray-200/60">
                  <button
                    onClick={handleRunBacktest}
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-4 rounded-xl hover:shadow-lg transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none transition-all duration-200 flex items-center justify-center space-x-3 text-lg font-semibold"
                  >
                    <Play className="w-5 h-5" />
                    <span>{loading ? 'Running Backtest...' : 'Run Backtest Analysis'}</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Strategy Templates */}
            <div className="xl:col-span-1">
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-6 sticky top-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-purple-600" />
                  Quick Templates
                </h3>
                <div className="space-y-3">
                  {[
                    { name: 'Momentum Strategy', type: 'momentum', description: 'Follow trending assets with momentum signals', color: 'blue' },
                    { name: 'Mean Reversion', type: 'mean_reversion', description: 'Bet on price normalization in oversold assets', color: 'green' },
                    { name: 'Quality Factor', type: 'factor', description: 'Invest in high-quality companies with strong fundamentals', color: 'purple' }
                  ].map((template, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setConfig({
                          ...config,
                          strategyType: template.type,
                          strategyName: template.name
                        });
                      }}
                      className={`w-full text-left p-4 border rounded-xl transition-all duration-200 hover:shadow-md group ${
                        template.color === 'blue' 
                          ? 'border-blue-200 hover:border-blue-300 bg-blue-50/50 hover:bg-blue-50' 
                          : template.color === 'green'
                          ? 'border-green-200 hover:border-green-300 bg-green-50/50 hover:bg-green-50'
                          : 'border-purple-200 hover:border-purple-300 bg-purple-50/50 hover:bg-purple-50'
                      }`}
                    >
                      <div className={`font-semibold mb-1 group-hover:translate-x-1 transition-transform ${
                        template.color === 'blue' ? 'text-blue-900' :
                        template.color === 'green' ? 'text-green-900' : 'text-purple-900'
                      }`}>
                        {template.name}
                      </div>
                      <div className={`text-sm ${
                        template.color === 'blue' ? 'text-blue-700' :
                        template.color === 'green' ? 'text-green-700' : 'text-purple-700'
                      }`}>
                        {template.description}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}

        {/* Results Panel */}
        {activeTab === 'results' && backtestResults && (
          <div className="xl:col-span-3 space-y-6 md:space-y-8">
            {/* Key Metrics */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-6 md:p-8">
              <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-6">
                Performance Summary
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
                {getMetrics().map((metric) => {
                  const Icon = metric.icon;
                  return (
                    <div key={metric.key} className="text-center p-4 bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200/60 hover:shadow-md transition-all duration-200">
                      <Icon className={`w-6 h-6 mx-auto mb-2 ${
                        metric.trend === 'up' ? 'text-green-600' : 
                        metric.trend === 'down' ? 'text-red-600' : 'text-gray-600'
                      }`} />
                      <div className="text-sm text-gray-600 mb-1 font-medium">{metric.label}</div>
                      <div className={`text-lg font-bold ${
                        metric.trend === 'up' ? 'text-green-600' : 
                        metric.trend === 'down' ? 'text-red-600' : 'text-gray-900'
                      }`}>
                        {formatMetricValue(metric.value)}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Charts and Detailed Analysis */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 md:gap-8">
              {/* Equity Curve */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Equity Curve</h3>
                <div className="h-80">
                  <Line data={getEquityChartData()} options={equityChartOptions} />
                </div>
              </div>

              {/* Drawdown Chart */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Drawdown Analysis</h3>
                <div className="h-80">
                  <Line data={getDrawdownChartData()} options={drawdownChartOptions} />
                </div>
              </div>

              {/* Recent Trades */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Recent Trades</h3>
                  <span className="text-sm text-gray-500">{backtestResults.trades.length} trades</span>
                </div>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {backtestResults.trades.slice(0, 10).map((trade) => (
                    <div key={trade.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors border border-gray-200/60">
                      <div className="flex items-center gap-4">
                        <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                          trade.action === 'BUY' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                        }`}>
                          {trade.action === 'BUY' ? 'B' : 'S'}
                        </div>
                        <div>
                          <div className="font-semibold text-gray-900">{trade.symbol}</div>
                          <div className="text-sm text-gray-500">
                            {trade.quantity} shares @ ${trade.price.toFixed(2)}
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`font-bold text-lg ${
                          trade.pnl >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                        </div>
                        <div className="text-sm text-gray-500">
                          {trade.timestamp.toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Risk Analysis */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Metrics</h3>
                <div className="space-y-4">
                  {[
                    { label: 'Value at Risk (95%)', value: '-5.2%', color: 'red' },
                    { label: 'Conditional VaR', value: '-7.8%', color: 'red' },
                    { label: 'Tail Ratio', value: '0.89', color: 'green' },
                    { label: 'Skewness', value: '-0.23', color: 'yellow' },
                    { label: 'Kurtosis', value: '3.45', color: 'yellow' },
                    { label: 'Information Ratio', value: '0.78', color: 'green' }
                  ].map((metric, index) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <span className="text-gray-700 font-medium">{metric.label}</span>
                      <span className={`font-semibold ${
                        metric.color === 'green' ? 'text-green-600' :
                        metric.color === 'red' ? 'text-red-600' : 'text-yellow-600'
                      }`}>
                        {metric.value}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Saved Strategies */}
        {activeTab === 'saved' && (
          <div className="xl:col-span-3">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-6 md:p-8">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
                <div>
                  <h3 className="text-xl md:text-2xl font-bold text-gray-900">
                    Saved Strategies
                  </h3>
                  <p className="text-gray-600 mt-1">Manage your strategy configurations</p>
                </div>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={strategyName}
                    onChange={(e) => setStrategyName(e.target.value)}
                    placeholder="Strategy name"
                    className="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 bg-white/80"
                  />
                  <button
                    onClick={handleSaveStrategy}
                    disabled={!strategyName.trim()}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                  >
                    Save Current
                  </button>
                </div>
              </div>

              {savedStrategies.length === 0 ? (
                <div className="text-center py-16 text-gray-500">
                  <Save className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p className="text-lg font-medium mb-2">No saved strategies yet</p>
                  <p className="text-gray-600">Save your current configuration to get started</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {savedStrategies.map((strategy) => (
                    <div key={strategy.id} className="border border-gray-200 rounded-xl p-6 hover:border-blue-300 hover:shadow-md transition-all duration-200 bg-gradient-to-br from-gray-50 to-white">
                      <div className="flex justify-between items-start mb-4">
                        <h4 className="font-bold text-gray-900 text-lg">{strategy.name}</h4>
                        <button
                          onClick={() => handleLoadStrategy(strategy)}
                          className="text-blue-600 hover:text-blue-700 text-sm font-medium bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg transition-colors"
                        >
                          Load
                        </button>
                      </div>
                      <div className="space-y-3 text-sm text-gray-600">
                        <div className="flex justify-between">
                          <span>Capital:</span>
                          <span className="font-semibold">${strategy.config.initialCapital.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Period:</span>
                          <span className="font-semibold">{strategy.config.startDate} to {strategy.config.endDate}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Assets:</span>
                          <span className="font-semibold">{strategy.config.symbols.length} symbols</span>
                        </div>
                        <div className="pt-3 border-t border-gray-200">
                          <div className="text-xs text-gray-500">
                            Created: {new Date(strategy.createdAt).toLocaleDateString()}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Empty State for Results */}
        {activeTab === 'results' && !backtestResults && (
          <div className="xl:col-span-3">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200/60 p-12 md:p-16 text-center">
              <div className="max-w-md mx-auto">
                <BarChart3 className="w-20 h-20 text-gray-400 mx-auto mb-6" />
                <h3 className="text-2xl font-bold text-gray-900 mb-3">No Results Yet</h3>
                <p className="text-gray-600 mb-8 text-lg">
                  Configure and run a backtest to see detailed performance results and analytics
                </p>
                <button
                  onClick={() => setActiveTab('configuration')}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 rounded-xl hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 inline-flex items-center gap-3 text-lg font-semibold"
                >
                  <Settings className="w-5 h-5" />
                  Configure Strategy
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BacktestStudio;