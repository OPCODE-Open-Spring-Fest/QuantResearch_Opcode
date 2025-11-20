import React, { useState, useEffect } from 'react';
import { Header } from '../components/Header';
import { 
  TrendingUp, 
  TrendingDown, 
  Target, 
  BarChart3, 
  Clock, 
  Activity, 
  Users, 
  Calendar, 
  ArrowRight,
  PlayCircle,
  Settings,
  PieChart,
  DollarSign,
  AlertCircle,
  CheckCircle2,
  XCircle,
  RefreshCw
} from 'lucide-react';

export const Dashboard = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('1M');
  const [activeTab, setActiveTab] = useState('overview');

  // Simulate loading
  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 1000);
    return () => clearTimeout(timer);
  }, []);

  const metrics = [
    { 
      title: 'Total Return', 
      value: '+23.45%', 
      change: '+2.1%', 
      icon: TrendingUp, 
      trend: 'up',
      description: 'Overall portfolio performance',
      color: 'green'
    },
    { 
      title: 'Sharpe Ratio', 
      value: '1.234', 
      change: '+0.12', 
      icon: TrendingUp, 
      trend: 'up',
      description: 'Risk-adjusted returns',
      color: 'blue'
    },
    { 
      title: 'Max Drawdown', 
      value: '-12.34%', 
      change: '-1.2%', 
      icon: TrendingDown, 
      trend: 'down',
      description: 'Maximum loss from peak',
      color: 'red'
    },
    { 
      title: 'Win Rate', 
      value: '64.50%', 
      change: '+3.2%', 
      icon: Target, 
      trend: 'up',
      description: 'Successful trade percentage',
      color: 'purple'
    },
    { 
      title: 'Volatility', 
      value: '18.2%', 
      change: '-0.8%', 
      icon: Activity, 
      trend: 'down',
      description: 'Portfolio risk measure',
      color: 'orange'
    },
    { 
      title: 'Alpha', 
      value: '2.34%', 
      change: '+0.45%', 
      icon: DollarSign, 
      trend: 'up',
      description: 'Excess returns over benchmark',
      color: 'indigo'
    }
  ];

  const recentBacktests = [
    { 
      id: 1,
      name: 'Momentum Strategy', 
      date: '2 hours ago', 
      status: 'completed',
      returns: '+5.2%',
      duration: '45 min',
      algorithm: 'ML-Based',
      assets: ['AAPL', 'GOOGL', 'MSFT']
    },
    { 
      id: 2,
      name: 'Mean Reversion', 
      date: '5 hours ago', 
      status: 'completed',
      returns: '+3.8%',
      duration: '1.2 hrs',
      algorithm: 'Statistical',
      assets: ['TSLA', 'NVDA', 'AMD']
    },
    { 
      id: 3,
      name: 'Sector Rotation', 
      date: '1 day ago', 
      status: 'running',
      returns: '-',
      duration: '3.5 hrs',
      algorithm: 'Sector-Based',
      assets: ['XLK', 'XLV', 'XLF']
    },
    { 
      id: 4,
      name: 'Volatility Arbitrage', 
      date: '2 days ago', 
      status: 'completed',
      returns: '+7.1%',
      duration: '2.1 hrs',
      algorithm: 'Options-Based',
      assets: ['SPY', 'VIX']
    }
  ];

  const quickActions = [
    {
      title: 'Run New Backtest',
      description: 'Test a new trading strategy',
      icon: PlayCircle,
      color: 'blue',
      onClick: () => console.log('Run backtest')
    },
    {
      title: 'Analyze Portfolio',
      description: 'Deep dive into performance metrics',
      icon: PieChart,
      color: 'green',
      onClick: () => console.log('Analyze portfolio')
    },
    {
      title: 'Research Factors',
      description: 'Explore alpha factors and signals',
      icon: Target,
      color: 'purple',
      onClick: () => console.log('Research factors')
    },
    {
      title: 'Optimize Parameters',
      description: 'Fine-tune strategy parameters',
      icon: Settings,
      color: 'orange',
      onClick: () => console.log('Optimize parameters')
    }
  ];

  const performanceData = [
    { month: 'Jan', return: 2.1, benchmark: 1.8 },
    { month: 'Feb', return: 3.2, benchmark: 2.5 },
    { month: 'Mar', return: -1.5, benchmark: -0.8 },
    { month: 'Apr', return: 4.8, benchmark: 3.2 },
    { month: 'May', return: 2.3, benchmark: 1.9 },
    { month: 'Jun', return: 5.1, benchmark: 4.2 },
    { month: 'Jul', return: 3.7, benchmark: 2.8 },
    { month: 'Aug', return: 2.9, benchmark: 2.1 }
  ];

  const marketOverview = [
    { asset: 'S&P 500', value: '4,567.89', change: '+1.2%', trend: 'up', volume: '2.3B' },
    { asset: 'NASDAQ', value: '14,235.67', change: '+2.1%', trend: 'up', volume: '1.8B' },
    { asset: 'BTC/USD', value: '$43,210', change: '-3.2%', trend: 'down', volume: '28.5K' },
    { asset: 'VIX', value: '15.23', change: '-0.8%', trend: 'down', volume: '0.5M' }
  ];

  const systemStatus = {
    liveTrading: { status: 'active', message: 'All systems operational' },
    dataFeeds: { status: 'active', message: 'Real-time data streaming' },
    backtestEngine: { status: 'degraded', message: 'High load - 85% capacity' },
    riskMonitor: { status: 'active', message: 'No alerts triggered' }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active': return <CheckCircle2 className="w-4 h-4 text-green-500" />;
      case 'degraded': return <AlertCircle className="w-4 h-4 text-yellow-500" />;
      case 'error': return <XCircle className="w-4 h-4 text-red-500" />;
      default: return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-50 border-green-200';
      case 'degraded': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'error': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
      {/* Header Section */}
      {/* <Header/> */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8 gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Welcome to your quantitative research workspace</p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          {/* Time Range Selector */}
          <div className="flex bg-white rounded-lg border border-gray-200 p-1">
            {['1D', '1W', '1M', '3M', '1Y'].map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
                  timeRange === range
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {range}
              </button>
            ))}
          </div>
          
          <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
            <Calendar className="w-4 h-4" />
            Generate Report
          </button>
          <button className="flex items-center gap-2 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-4 py-2 rounded-lg transition-colors duration-200">
            <Users className="w-4 h-4" />
            Team Analytics
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 md:gap-6 mb-8">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <div 
              key={index} 
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 md:p-6 hover:shadow-md transition-all duration-200 transform hover:-translate-y-1"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`p-2 rounded-lg ${
                  metric.trend === 'up' ? 'bg-green-50' : 'bg-red-50'
                }`}>
                  <Icon className={`w-5 h-5 md:w-6 md:h-6 ${
                    metric.trend === 'up' ? 'text-green-600' : 'text-red-600'
                  }`} />
                </div>
                <span className={`text-sm font-medium ${
                  metric.trend === 'up' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {metric.change}
                </span>
              </div>
              <h3 className="text-gray-600 text-sm font-medium mb-1">
                {metric.title}
              </h3>
              <div className={`text-xl md:text-2xl font-bold mb-2 ${
                metric.trend === 'up' ? 'text-green-600' : 'text-red-600'
              }`}>
                {metric.value}
              </div>
              <p className="text-gray-500 text-xs">
                {metric.description}
              </p>
            </div>
          );
        })}
      </div>

      {/* System Status */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(systemStatus).map(([key, value]) => (
            <div key={key} className={`flex items-center gap-3 p-3 rounded-lg border ${getStatusColor(value.status)}`}>
              {getStatusIcon(value.status)}
              <div>
                <div className="font-medium capitalize">{key.replace(/([A-Z])/g, ' $1')}</div>
                <div className="text-sm opacity-75">{value.message}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 md:gap-8">
        {/* Performance Chart */}
        <div className="xl:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
            <h3 className="text-lg md:text-xl font-semibold text-gray-900">
              Performance Overview
            </h3>
            <div className="flex gap-2">
              <select 
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full sm:w-auto p-2.5"
              >
                <option value="1D">1 Day</option>
                <option value="1W">1 Week</option>
                <option value="1M">1 Month</option>
                <option value="3M">3 Months</option>
                <option value="1Y">1 Year</option>
              </select>
            </div>
          </div>
          <div className="h-64 md:h-80">
            <div className="flex items-end justify-between h-full pb-4">
              {performanceData.map((data, index) => (
                <div key={index} className="flex flex-col items-center gap-2 flex-1">
                  <div className="flex flex-col items-center gap-1 w-full">
                    {/* Benchmark Bar */}
                    <div 
                      className="w-full bg-blue-200 rounded-t transition-all duration-300 hover:bg-blue-300"
                      style={{ height: `${Math.max(data.benchmark * 8, 4)}px` }}
                      title={`Benchmark: ${data.benchmark}%`}
                    />
                    {/* Strategy Bar */}
                    <div 
                      className={`w-full rounded-t transition-all duration-300 hover:opacity-80 ${
                        data.return >= 0 ? 'bg-green-500' : 'bg-red-500'
                      }`}
                      style={{ height: `${Math.max(Math.abs(data.return) * 8, 4)}px` }}
                      title={`Strategy: ${data.return}%`}
                    />
                  </div>
                  <span className="text-xs text-gray-500 font-medium">
                    {data.month}
                  </span>
                </div>
              ))}
            </div>
            <div className="flex justify-center gap-6 mt-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded"></div>
                <span className="text-sm text-gray-600">Strategy</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-200 rounded"></div>
                <span className="text-sm text-gray-600">Benchmark</span>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Backtests */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg md:text-xl font-semibold text-gray-900">
              Recent Backtests
            </h3>
            <button className="flex items-center gap-1 text-blue-600 hover:text-blue-700 text-sm font-medium">
              View All <ArrowRight className="w-4 h-4" />
            </button>
          </div>
          <div className="space-y-4">
            {recentBacktests.map((test) => (
              <div 
                key={test.id} 
                className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 border border-gray-200"
              >
                <div className="flex flex-col gap-3">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="font-semibold text-gray-900 mb-1">
                        {test.name}
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
                        <Clock className="w-4 h-4" />
                        <span>{test.date}</span>
                        <span>•</span>
                        <span>{test.duration}</span>
                      </div>
                      <div className="flex flex-wrap gap-1 mb-2">
                        {test.assets.slice(0, 3).map((asset, idx) => (
                          <span 
                            key={idx}
                            className="px-2 py-1 bg-white border border-gray-300 rounded text-xs text-gray-600"
                          >
                            {asset}
                          </span>
                        ))}
                        {test.assets.length > 3 && (
                          <span className="px-2 py-1 bg-white border border-gray-300 rounded text-xs text-gray-600">
                            +{test.assets.length - 3}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      {test.returns !== '-' && (
                        <span className={`text-sm font-semibold ${
                          test.returns.startsWith('+') 
                            ? 'text-green-600' 
                            : 'text-red-600'
                        }`}>
                          {test.returns}
                        </span>
                      )}
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        test.status === 'completed' 
                          ? 'bg-green-100 text-green-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}>
                        {test.status}
                      </span>
                    </div>
                  </div>
                  <div className="text-xs text-gray-500">
                    Algorithm: {test.algorithm}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg md:text-xl font-semibold text-gray-900 mb-6">
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-1 gap-4">
            {quickActions.map((action, index) => {
              const ActionIcon = action.icon;
              return (
                <button
                  key={index}
                  onClick={action.onClick}
                  className={`flex items-center gap-4 p-4 rounded-lg border transition-all duration-200 hover:shadow-md group ${
                    action.color === 'blue' 
                      ? 'border-blue-200 bg-blue-50 hover:bg-blue-100' 
                      : action.color === 'green'
                      ? 'border-green-200 bg-green-50 hover:bg-green-100'
                      : action.color === 'purple'
                      ? 'border-purple-200 bg-purple-50 hover:bg-purple-100'
                      : 'border-orange-200 bg-orange-50 hover:bg-orange-100'
                  }`}
                >
                  <div className={`p-2 rounded-lg transition-colors group-hover:scale-110 ${
                    action.color === 'blue' 
                      ? 'bg-blue-100 text-blue-600 group-hover:bg-blue-200' 
                      : action.color === 'green'
                      ? 'bg-green-100 text-green-600 group-hover:bg-green-200'
                      : action.color === 'purple'
                      ? 'bg-purple-100 text-purple-600 group-hover:bg-purple-200'
                      : 'bg-orange-100 text-orange-600 group-hover:bg-orange-200'
                  }`}>
                    <ActionIcon className="w-5 h-5" />
                  </div>
                  <div className="flex-1 text-left">
                    <div className={`font-semibold ${
                      action.color === 'blue' 
                        ? 'text-blue-900' 
                        : action.color === 'green'
                        ? 'text-green-900'
                        : action.color === 'purple'
                        ? 'text-purple-900'
                        : 'text-orange-900'
                    }`}>
                      {action.title}
                    </div>
                    <div className={`text-sm ${
                      action.color === 'blue' 
                        ? 'text-blue-700' 
                        : action.color === 'green'
                        ? 'text-green-700'
                        : action.color === 'purple'
                        ? 'text-purple-700'
                        : 'text-orange-700'
                    }`}>
                      {action.description}
                    </div>
                  </div>
                  <ArrowRight className={`w-4 h-4 transition-transform group-hover:translate-x-1 ${
                    action.color === 'blue' 
                      ? 'text-blue-600' 
                      : action.color === 'green'
                      ? 'text-green-600'
                      : action.color === 'purple'
                      ? 'text-purple-600'
                      : 'text-orange-600'
                  }`} />
                </button>
              );
            })}
          </div>
        </div>

        {/* Market Overview */}
        <div className="xl:col-span-3 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg md:text-xl font-semibold text-gray-900">
              Market Overview
            </h3>
            <span className="text-sm text-gray-500">Live</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {marketOverview.map((item, index) => (
              <div 
                key={index} 
                className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 border border-gray-200"
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="text-sm font-medium text-gray-900">
                    {item.asset}
                  </div>
                  <div className={`text-xs font-semibold px-2 py-1 rounded ${
                    item.trend === 'up' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {item.change}
                  </div>
                </div>
                <div className="text-lg font-bold text-gray-900 mb-1">
                  {item.value}
                </div>
                <div className="text-xs text-gray-500">
                  Volume: {item.volume}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};