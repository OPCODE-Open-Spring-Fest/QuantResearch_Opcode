import React, { useState, useEffect } from 'react';
import { 
  PieChart, 
  BarChart, 
  TrendingUp, 
  TrendingDown,
  DollarSign,
  Shield,
  Target,
  Activity,
  Calendar,
  Download,
  Filter,
  RefreshCw,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';

export const PortfolioAnalytics = () => {
  const [timeRange, setTimeRange] = useState('1M');
  const [isLoading, setIsLoading] = useState(true);

  // Simulate loading
  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 1500);
    return () => clearTimeout(timer);
  }, []);

  // Mock data
  const assetAllocation = [
    { name: 'US Stocks', value: 45, color: '#3B82F6' },
    { name: 'International', value: 25, color: '#10B981' },
    { name: 'Bonds', value: 15, color: '#8B5CF6' },
    { name: 'Cash', value: 8, color: '#F59E0B' },
    { name: 'Alternatives', value: 7, color: '#EF4444' }
  ];

  const sectorExposure = [
    { sector: 'Technology', weight: 32, change: '+2.1%' },
    { sector: 'Healthcare', weight: 18, change: '+0.8%' },
    { sector: 'Financials', weight: 15, change: '-1.2%' },
    { sector: 'Consumer', weight: 12, change: '+0.5%' },
    { sector: 'Industrial', weight: 10, change: '-0.3%' },
    { sector: 'Energy', weight: 8, change: '+1.7%' },
    { sector: 'Other', weight: 5, change: '-0.2%' }
  ];

  const riskMetrics = [
    { metric: 'Value at Risk (95%)', value: '-5.2%', trend: 'down', description: 'Maximum expected loss over 1 day' },
    { metric: 'Expected Shortfall', value: '-7.8%', trend: 'down', description: 'Average loss beyond VaR' },
    { metric: 'Beta to Market', value: '1.12', trend: 'up', description: 'Sensitivity to market movements' },
    { metric: 'Tracking Error', value: '4.5%', trend: 'neutral', description: 'Deviation from benchmark' },
    { metric: 'Sharpe Ratio', value: '1.45', trend: 'up', description: 'Risk-adjusted returns' },
    { metric: 'Sortino Ratio', value: '2.12', trend: 'up', description: 'Downside risk adjustment' }
  ];

  const performanceAttribution = [
    { factor: 'Stock Selection', contribution: '+3.2%', impact: 'positive' },
    { factor: 'Sector Allocation', contribution: '+1.8%', impact: 'positive' },
    { factor: 'Currency Effects', contribution: '-0.4%', impact: 'negative' },
    { factor: 'Transaction Costs', contribution: '-0.9%', impact: 'negative' },
    { factor: 'Market Timing', contribution: '+2.1%', impact: 'positive' },
    { factor: 'Risk Management', contribution: '+0.7%', impact: 'positive' }
  ];

  const portfolioStats = [
    { title: 'Total Value', value: '$2,456,789', change: '+5.2%', icon: DollarSign, trend: 'up' },
    { title: 'Daily P&L', value: '+$12,345', change: '+2.1%', icon: TrendingUp, trend: 'up' },
    { title: 'YTD Return', value: '+18.3%', change: '+3.4%', icon: Activity, trend: 'up' },
    { title: 'Risk Score', value: '7.2/10', change: '-0.3', icon: Shield, trend: 'down' }
  ];

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading portfolio analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
      {/* Header Section */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8 gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900">Portfolio Analytics</h1>
          <p className="text-gray-600 mt-2">Deep dive into portfolio performance and risk metrics</p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          {/* Time Range Selector */}
          <div className="flex bg-white rounded-lg border border-gray-200 p-1">
            {['1D', '1W', '1M', '3M', '1Y', 'ALL'].map((range) => (
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
          
          <button className="flex items-center gap-2 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-4 py-2 rounded-lg transition-colors">
            <Filter className="w-4 h-4" />
            Filter
          </button>
          <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
            <Download className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      {/* Portfolio Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
        {portfolioStats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div 
              key={index} 
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 md:p-6 hover:shadow-md transition-all duration-200"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`p-2 rounded-lg ${
                  stat.trend === 'up' ? 'bg-green-50' : 'bg-red-50'
                }`}>
                  <Icon className={`w-5 h-5 md:w-6 md:h-6 ${
                    stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                  }`} />
                </div>
                <span className={`text-sm font-medium ${
                  stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {stat.change}
                </span>
              </div>
              <h3 className="text-gray-600 text-sm font-medium mb-1">
                {stat.title}
              </h3>
              <div className="text-xl md:text-2xl font-bold text-gray-900">
                {stat.value}
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Analytics Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 md:gap-8">
        {/* Left Column */}
        <div className="space-y-6 md:space-y-8">
          {/* Asset Allocation */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg md:text-xl font-semibold text-gray-900">
                Asset Allocation
              </h3>
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                View Details
              </button>
            </div>
            <div className="flex flex-col lg:flex-row items-center gap-6">
              {/* Pie Chart Placeholder */}
              <div className="relative w-48 h-48 flex items-center justify-center">
                <div className="absolute inset-0 rounded-full border-8 border-gray-200"></div>
                <div className="absolute inset-4 rounded-full border-8 border-blue-500"></div>
                <div className="absolute inset-8 rounded-full border-8 border-green-500"></div>
                <div className="absolute inset-12 rounded-full border-8 border-purple-500"></div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">100%</div>
                  <div className="text-sm text-gray-500">Total</div>
                </div>
              </div>
              
              {/* Allocation Breakdown */}
              <div className="flex-1 min-w-0">
                <div className="space-y-3">
                  {assetAllocation.map((asset, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: asset.color }}
                        />
                        <span className="text-sm font-medium text-gray-700">
                          {asset.name}
                        </span>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-semibold text-gray-900">
                          {asset.value}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Risk Analysis */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg md:text-xl font-semibold text-gray-900">
                Risk Analysis
              </h3>
              <Shield className="w-5 h-5 text-gray-400" />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {riskMetrics.map((metric, index) => (
                <div 
                  key={index} 
                  className="p-4 bg-gray-50 rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">
                      {metric.metric}
                    </span>
                    {metric.trend === 'up' && (
                      <ArrowUpRight className="w-4 h-4 text-green-500" />
                    )}
                    {metric.trend === 'down' && (
                      <ArrowDownRight className="w-4 h-4 text-red-500" />
                    )}
                  </div>
                  <div className="text-lg font-bold text-gray-900 mb-1">
                    {metric.value}
                  </div>
                  <div className="text-xs text-gray-500">
                    {metric.description}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6 md:space-y-8">
          {/* Sector Exposure */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg md:text-xl font-semibold text-gray-900">
                Sector Exposure
              </h3>
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                Compare
              </button>
            </div>
            <div className="space-y-4">
              {sectorExposure.map((sector, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-700">
                      {sector.sector}
                    </span>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-semibold text-gray-900">
                        {sector.weight}%
                      </span>
                      <span className={`text-xs font-medium ${
                        sector.change.startsWith('+') 
                          ? 'text-green-600' 
                          : 'text-red-600'
                      }`}>
                        {sector.change}
                      </span>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${sector.weight}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Performance Attribution */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-lg md:text-xl font-semibold text-gray-900">
                Performance Attribution
              </h3>
              <Target className="w-5 h-5 text-gray-400" />
            </div>
            <div className="space-y-4">
              {performanceAttribution.map((item, index) => (
                <div 
                  key={index} 
                  className="flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <span className="text-gray-700 font-medium">
                    {item.factor}
                  </span>
                  <span className={`font-semibold ${
                    item.impact === 'positive'
                      ? 'text-green-600'
                      : 'text-red-600'
                  }`}>
                    {item.contribution}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PortfolioAnalytics;