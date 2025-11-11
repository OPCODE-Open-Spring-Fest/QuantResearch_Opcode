import React from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Target, 
  BarChart3, 
  Clock, 
  Activity, 
  Users, 
  Calendar, 
  ArrowRight,
  PlayCircle,
  Settings,
  PieChart
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const metrics = [
    { 
      title: 'Total Return', 
      value: '+23.45%', 
      change: '+2.1%', 
      icon: TrendingUp, 
      trend: 'up',
      description: 'Overall portfolio performance'
    },
    { 
      title: 'Sharpe Ratio', 
      value: '1.234', 
      change: '+0.12', 
      icon: TrendingUp, 
      trend: 'up',
      description: 'Risk-adjusted returns'
    },
    { 
      title: 'Max Drawdown', 
      value: '-12.34%', 
      change: '-1.2%', 
      icon: TrendingDown, 
      trend: 'down',
      description: 'Maximum loss from peak'
    },
    { 
      title: 'Win Rate', 
      value: '64.50%', 
      change: '+3.2%', 
      icon: Target, 
      trend: 'up',
      description: 'Successful trade percentage'
    },
    { 
      title: 'Volatility', 
      value: '18.2%', 
      change: '-0.8%', 
      icon: Activity, 
      trend: 'down',
      description: 'Portfolio risk measure'
    },
    { 
      title: 'Alpha', 
      value: '2.34%', 
      change: '+0.45%', 
      icon: TrendingUp, 
      trend: 'up',
      description: 'Excess returns over benchmark'
    }
  ];

  const recentBacktests = [
    { 
      name: 'Momentum Strategy', 
      date: '2 hours ago', 
      status: 'Completed',
      returns: '+5.2%',
      duration: '45 min'
    },
    { 
      name: 'Mean Reversion', 
      date: '5 hours ago', 
      status: 'Completed',
      returns: '+3.8%',
      duration: '1.2 hrs'
    },
    { 
      name: 'Sector Rotation', 
      date: '1 day ago', 
      status: 'Running',
      returns: '-',
      duration: '3.5 hrs'
    },
    { 
      name: 'Volatility Arbitrage', 
      date: '2 days ago', 
      status: 'Completed',
      returns: '+7.1%',
      duration: '2.1 hrs'
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
    { month: 'Jan', return: 2.1 },
    { month: 'Feb', return: 3.2 },
    { month: 'Mar', return: -1.5 },
    { month: 'Apr', return: 4.8 },
    { month: 'May', return: 2.3 },
    { month: 'Jun', return: 5.1 },
    { month: 'Jul', return: 3.7 },
    { month: 'Aug', return: 2.9 }
  ];

  const marketData = [
    { asset: 'S&P 500', value: '4,567.89', change: '+1.2%', trend: 'up' },
    { asset: 'NASDAQ', value: '14,235.67', change: '+2.1%', trend: 'up' },
    { asset: 'BTC/USD', value: '$43,210', change: '-3.2%', trend: 'down' },
    { asset: 'VIX', value: '15.23', change: '-0.8%', trend: 'down' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 md:p-6 lg:p-8">
      {/* Header Section */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8 gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Welcome to your quantitative research workspace
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
            <Calendar className="w-4 h-4" />
            Generate Report
          </button>
          <button className="flex items-center gap-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg transition-colors duration-200">
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
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 md:p-6 hover:shadow-md transition-shadow duration-200"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`p-2 rounded-lg ${
                  metric.trend === 'up' ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20'
                }`}>
                  <Icon className={`w-5 h-5 md:w-6 md:h-6 ${
                    metric.trend === 'up' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                  }`} />
                </div>
                <span className={`text-sm font-medium ${
                  metric.trend === 'up' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                }`}>
                  {metric.change}
                </span>
              </div>
              <h3 className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-1">
                {metric.title}
              </h3>
              <div className={`text-xl md:text-2xl font-bold mb-2 ${
                metric.trend === 'up' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
              }`}>
                {metric.value}
              </div>
              <p className="text-gray-400 dark:text-gray-500 text-xs">
                {metric.description}
              </p>
            </div>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 md:gap-8">
        {/* Performance Chart - Full width on xl screens */}
        <div className="xl:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
            <h3 className="text-lg md:text-xl font-semibold text-gray-900 dark:text-white">
              Performance Overview
            </h3>
            <select className="bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full sm:w-auto p-2.5">
              <option>1 Month</option>
              <option>3 Months</option>
              <option>1 Year</option>
              <option>YTD</option>
            </select>
          </div>
          <div className="h-64 md:h-80 flex items-center justify-center">
            <div className="text-center">
              <BarChart3 className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
              <p className="text-gray-500 dark:text-gray-400 mb-4">
                Performance chart visualization
              </p>
              <div className="flex items-end justify-center gap-2 h-32">
                {performanceData.map((data, index) => (
                  <div key={index} className="flex flex-col items-center gap-2">
                    <div 
                      className={`w-6 md:w-8 rounded-t ${
                        data.return >= 0 
                          ? 'bg-green-500 dark:bg-green-400' 
                          : 'bg-red-500 dark:bg-red-400'
                      }`}
                      style={{ height: `${Math.abs(data.return) * 8}px` }}
                    ></div>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {data.month}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Recent Backtests */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg md:text-xl font-semibold text-gray-900 dark:text-white">
              Recent Backtests
            </h3>
            <button className="flex items-center gap-1 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 text-sm font-medium">
              View All <ArrowRight className="w-4 h-4" />
            </button>
          </div>
          <div className="space-y-4">
            {recentBacktests.map((test, index) => (
              <div 
                key={index} 
                className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
              >
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 dark:text-white mb-1">
                      {test.name}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                      <Clock className="w-4 h-4" />
                      <span>{test.date}</span>
                      <span>•</span>
                      <span>{test.duration}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {test.returns !== '-' && (
                      <span className={`text-sm font-medium ${
                        test.returns.startsWith('+') 
                          ? 'text-green-600 dark:text-green-400' 
                          : 'text-red-600 dark:text-red-400'
                      }`}>
                        {test.returns}
                      </span>
                    )}
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      test.status === 'Completed' 
                        ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400'
                        : 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-400'
                    }`}>
                      {test.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg md:text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Quick Actions
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-1 gap-4">
            {quickActions.map((action, index) => {
              const ActionIcon = action.icon;
              return (
                <button
                  key={index}
                  onClick={action.onClick}
                  className={`flex items-center gap-4 p-4 rounded-lg border transition-all duration-200 hover:shadow-md ${
                    action.color === 'blue' 
                      ? 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/30' 
                      : action.color === 'green'
                      ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20 hover:bg-green-100 dark:hover:bg-green-900/30'
                      : action.color === 'purple'
                      ? 'border-purple-200 dark:border-purple-800 bg-purple-50 dark:bg-purple-900/20 hover:bg-purple-100 dark:hover:bg-purple-900/30'
                      : 'border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/20 hover:bg-orange-100 dark:hover:bg-orange-900/30'
                  }`}
                >
                  <div className={`p-2 rounded-lg ${
                    action.color === 'blue' 
                      ? 'bg-blue-100 dark:bg-blue-800 text-blue-600 dark:text-blue-400' 
                      : action.color === 'green'
                      ? 'bg-green-100 dark:bg-green-800 text-green-600 dark:text-green-400'
                      : action.color === 'purple'
                      ? 'bg-purple-100 dark:bg-purple-800 text-purple-600 dark:text-purple-400'
                      : 'bg-orange-100 dark:bg-orange-800 text-orange-600 dark:text-orange-400'
                  }`}>
                    <ActionIcon className="w-5 h-5" />
                  </div>
                  <div className="flex-1 text-left">
                    <div className={`font-medium ${
                      action.color === 'blue' 
                        ? 'text-blue-900 dark:text-blue-300' 
                        : action.color === 'green'
                        ? 'text-green-900 dark:text-green-300'
                        : action.color === 'purple'
                        ? 'text-purple-900 dark:text-purple-300'
                        : 'text-orange-900 dark:text-orange-300'
                    }`}>
                      {action.title}
                    </div>
                    <div className={`text-sm ${
                      action.color === 'blue' 
                        ? 'text-blue-700 dark:text-blue-400' 
                        : action.color === 'green'
                        ? 'text-green-700 dark:text-green-400'
                        : action.color === 'purple'
                        ? 'text-purple-700 dark:text-purple-400'
                        : 'text-orange-700 dark:text-orange-400'
                    }`}>
                      {action.description}
                    </div>
                  </div>
                  <ArrowRight className={`w-4 h-4 ${
                    action.color === 'blue' 
                      ? 'text-blue-600 dark:text-blue-400' 
                      : action.color === 'green'
                      ? 'text-green-600 dark:text-green-400'
                      : action.color === 'purple'
                      ? 'text-purple-600 dark:text-purple-400'
                      : 'text-orange-600 dark:text-orange-400'
                  }`} />
                </button>
              );
            })}
          </div>
        </div>

        {/* Market Overview */}
        <div className="xl:col-span-3 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg md:text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Market Overview
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {marketData.map((item, index) => (
              <div 
                key={index} 
                className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
              >
                <div className="text-sm text-gray-500 dark:text-gray-400 mb-1">
                  {item.asset}
                </div>
                <div className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                  {item.value}
                </div>
                <div className={`text-sm font-medium ${
                  item.trend === 'up' 
                    ? 'text-green-600 dark:text-green-400' 
                    : 'text-red-600 dark:text-red-400'
                }`}>
                  {item.change}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};