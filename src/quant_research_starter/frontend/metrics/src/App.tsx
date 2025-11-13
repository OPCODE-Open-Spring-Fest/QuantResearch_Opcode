//import React from 'react';
import { useBacktestData } from './hooks/useBacktestData';
import MetricCard from './components/MetricCard';
import PerformanceChart from './components/PerformanceChart';
import DrawdownChart from './components/DrawdownChart';
//import { RefreshCw, AlertCircle, Database } from 'lucide-react';

function App() {
  const { data, loading, error, refreshData } = useBacktestData();

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 max-w-md w-full text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Error Loading Data</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={refreshData}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
        </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <Database className="w-8 h-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Metrics Dashboard</h1>
            </div>
            <button
              onClick={refreshData}
              disabled={loading}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              {loading ? 'Refreshing...' : 'Refresh Data'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Total Return"
            value={data?.metrics.totalReturn || 0}
            format="percentage"
            description="Cumulative return over the period"
          />
          <MetricCard
            title="Sharpe Ratio"
            value={data?.metrics.sharpeRatio || 0}
            format="ratio"
            description="Risk-adjusted return"
          />
          <MetricCard
            title="Max Drawdown"
            value={data?.metrics.maxDrawdown || 0}
            format="percentage"
            description="Maximum peak-to-trough decline"
          />
          <MetricCard
            title="Volatility"
            value={data?.metrics.volatility || 0}
            format="percentage"
            description="Annualized standard deviation of returns"
          />
          <MetricCard
            title="Win Rate"
            value={data?.metrics.winRate || 0}
            format="percentage"
            description="Percentage of winning trades"
          />
          <MetricCard
            title="Profit Factor"
            value={data?.metrics.profitFactor || 0}
            format="ratio"
            description="Gross profit divided by gross loss"
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          <PerformanceChart
            data={data?.performance || []}
            loading={loading}
            height={400}
          />
          <DrawdownChart
            data={data?.drawdown || []}
            loading={loading}
            height={400}
          />
        </div>

        {/* Loading State */}
        {loading && !data && (
          <div className="fixed inset-0 bg-white bg-opacity-80 flex items-center justify-center z-50">
            <div className="text-center">
              <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
              <p className="text-lg font-medium text-gray-700">Loading metrics data...</p>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            Metrics Dashboard • Built with React, TypeScript, and Recharts
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;