import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Play } from 'lucide-react';
import { useQuantData } from '../hooks/useQuantData';
export const BacktestStudio = () => {
    const { loading, runBacktest, backtestResults } = useQuantData();
    const [config, setConfig] = useState({
        initialCapital: 100000,
        startDate: '2020-01-01',
        endDate: '2023-01-01',
        rebalanceFrequency: 'monthly',
        symbols: ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    });
    const handleRunBacktest = () => {
        runBacktest(config);
    };
    // Format metric value for display with proper typing
    const formatMetricValue = (value) => {
        if (typeof value === 'number') {
            // For ratios (like sharpe), don't add percentage
            if (value > 1 || value < -1) {
                return value.toFixed(3);
            }
            return (value * 100).toFixed(2) + '%';
        }
        return String(value);
    };
    // Safely get metrics with proper typing
    const getMetrics = () => {
        if (!backtestResults?.metrics)
            return [];
        const metrics = backtestResults.metrics;
        return [
            ['Total Return', formatMetricValue(metrics.totalReturn)],
            ['Annualized Return', formatMetricValue(metrics.annualizedReturn)],
            ['Volatility', formatMetricValue(metrics.volatility)],
            ['Sharpe Ratio', formatMetricValue(metrics.sharpeRatio)],
            ['Max Drawdown', formatMetricValue(metrics.maxDrawdown)],
            ['Win Rate', formatMetricValue(metrics.winRate)],
            ['Turnover', formatMetricValue(metrics.turnover)]
        ];
    };
    return (_jsxs("div", { className: "p-8", children: [_jsxs("div", { className: "mb-8", children: [_jsx("h1", { className: "text-3xl font-bold text-gray-900", children: "Backtest Studio" }), _jsx("p", { className: "text-gray-600 mt-2", children: "Test and optimize your trading strategies" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-8", children: [_jsx("div", { className: "lg:col-span-1", children: _jsxs("div", { className: "bg-white rounded-xl shadow-sm border border-gray-200 p-6", children: [_jsx("h3", { className: "text-lg font-semibold text-gray-900 mb-4", children: "Strategy Configuration" }), _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-sm font-medium text-gray-700 mb-2", children: "Initial Capital ($)" }), _jsx("input", { type: "number", value: config.initialCapital, onChange: (e) => setConfig({ ...config, initialCapital: Number(e.target.value) }), className: "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-sm font-medium text-gray-700 mb-2", children: "Start Date" }), _jsx("input", { type: "date", value: config.startDate, onChange: (e) => setConfig({ ...config, startDate: e.target.value }), className: "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-sm font-medium text-gray-700 mb-2", children: "End Date" }), _jsx("input", { type: "date", value: config.endDate, onChange: (e) => setConfig({ ...config, endDate: e.target.value }), className: "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-sm font-medium text-gray-700 mb-2", children: "Rebalance Frequency" }), _jsxs("select", { value: config.rebalanceFrequency, onChange: (e) => setConfig({
                                                        ...config,
                                                        rebalanceFrequency: e.target.value
                                                    }), className: "w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent", children: [_jsx("option", { value: "daily", children: "Daily" }), _jsx("option", { value: "weekly", children: "Weekly" }), _jsx("option", { value: "monthly", children: "Monthly" })] })] }), _jsxs("button", { onClick: handleRunBacktest, disabled: loading, className: "w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2", children: [_jsx(Play, { className: "w-4 h-4" }), _jsx("span", { children: loading ? 'Running...' : 'Run Backtest' })] })] })] }) }), _jsx("div", { className: "lg:col-span-2", children: _jsxs("div", { className: "bg-white rounded-xl shadow-sm border border-gray-200 p-6", children: [_jsx("h3", { className: "text-lg font-semibold text-gray-900 mb-4", children: "Backtest Results" }), loading ? (_jsxs("div", { className: "text-center py-12", children: [_jsx("div", { className: "animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" }), _jsx("p", { className: "text-gray-600", children: "Running backtest analysis..." })] })) : backtestResults ? (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-4", children: getMetrics().map(([key, value]) => (_jsxs("div", { className: "text-center p-4 bg-gray-50 rounded-lg", children: [_jsx("div", { className: "text-sm text-gray-600 capitalize", children: key }), _jsx("div", { className: "text-xl font-bold text-gray-900 mt-1", children: value })] }, key))) }), _jsxs("div", { className: "border-t pt-6", children: [_jsx("h4", { className: "font-semibold text-gray-900 mb-3", children: "Performance Chart" }), _jsx("div", { className: "h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500", children: "Performance chart will be displayed here" })] })] })) : (_jsxs("div", { className: "text-center py-12 text-gray-500", children: [_jsx(Play, { className: "w-12 h-12 mx-auto mb-4 opacity-50" }), _jsx("p", { children: "Configure and run a backtest to see results" })] }))] }) })] })] }));
};
