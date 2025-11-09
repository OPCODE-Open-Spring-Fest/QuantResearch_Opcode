import React from 'react';
import { TrendingUp, TrendingDown, DollarSign, Target } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const metrics = [
    { title: 'Total Return', value: '+23.45%', change: '+2.1%', icon: TrendingUp, trend: 'up' },
    { title: 'Sharpe Ratio', value: '1.234', change: '+0.12', icon: TrendingUp, trend: 'up' },
    { title: 'Max Drawdown', value: '-12.34%', change: '-1.2%', icon: TrendingDown, trend: 'down' },
    { title: 'Win Rate', value: '64.50%', change: '+3.2%', icon: Target, trend: 'up' }
  ];

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome to your quantitative research workspace</p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="p-2 bg-blue-50 rounded-lg">
                  <Icon className={`w-6 h-6 ${
                    metric.trend === 'up' ? 'text-green-600' : 'text-red-600'
                  }`} />
                </div>
                <span className={`text-sm font-medium ${
                  metric.trend === 'up' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {metric.change}
                </span>
              </div>
              <h3 className="text-gray-600 text-sm font-medium mb-1">{metric.title}</h3>
              <div className={`text-2xl font-bold ${
                metric.trend === 'up' ? 'text-green-600' : 'text-red-600'
              }`}>
                {metric.value}
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Backtests</h3>
          <div className="space-y-4">
            {[
              { name: 'Momentum Strategy', date: '2 hours ago', status: 'Completed' },
              { name: 'Mean Reversion', date: '5 hours ago', status: 'Completed' },
              { name: 'Sector Rotation', date: '1 day ago', status: 'Running' }
            ].map((test, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">{test.name}</div>
                  <div className="text-sm text-gray-500">{test.date}</div>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  test.status === 'Completed' 
                    ? 'bg-green-100 text-green-800'
                    : 'bg-blue-100 text-blue-800'
                }`}>
                  {test.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full text-left p-4 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors">
              <div className="font-medium text-blue-900">Run New Backtest</div>
              <div className="text-sm text-blue-700">Test a new trading strategy</div>
            </button>
            <button className="w-full text-left p-4 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors">
              <div className="font-medium text-green-900">Analyze Portfolio</div>
              <div className="text-sm text-green-700">Deep dive into performance metrics</div>
            </button>
            <button className="w-full text-left p-4 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 transition-colors">
              <div className="font-medium text-purple-900">Research Factors</div>
              <div className="text-sm text-purple-700">Explore alpha factors</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};