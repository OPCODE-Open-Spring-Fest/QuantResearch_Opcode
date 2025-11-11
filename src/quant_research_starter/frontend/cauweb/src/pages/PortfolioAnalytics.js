import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { PieChart, BarChart } from 'lucide-react';
export const PortfolioAnalytics = () => {
    return (_jsxs("div", { className: "p-8", children: [_jsxs("div", { className: "mb-8", children: [_jsx("h1", { className: "text-3xl font-bold text-gray-900", children: "Portfolio Analytics" }), _jsx("p", { className: "text-gray-600 mt-2", children: "Deep dive into portfolio performance and risk" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-8", children: [_jsxs("div", { className: "bg-white rounded-xl shadow-sm border border-gray-200 p-6", children: [_jsx("h3", { className: "text-lg font-semibold text-gray-900 mb-4", children: "Asset Allocation" }), _jsxs("div", { className: "h-64 flex items-center justify-center text-gray-500", children: [_jsx(PieChart, { className: "w-12 h-12 opacity-50 mr-4" }), _jsx("span", { children: "Allocation chart will be displayed here" })] })] }), _jsxs("div", { className: "bg-white rounded-xl shadow-sm border border-gray-200 p-6", children: [_jsx("h3", { className: "text-lg font-semibold text-gray-900 mb-4", children: "Sector Exposure" }), _jsxs("div", { className: "h-64 flex items-center justify-center text-gray-500", children: [_jsx(BarChart, { className: "w-12 h-12 opacity-50 mr-4" }), _jsx("span", { children: "Sector exposure chart will be displayed here" })] })] }), _jsxs("div", { className: "bg-white rounded-xl shadow-sm border border-gray-200 p-6", children: [_jsx("h3", { className: "text-lg font-semibold text-gray-900 mb-4", children: "Risk Analysis" }), _jsx("div", { className: "space-y-4", children: [
                                    { metric: 'Value at Risk (95%)', value: '-5.2%' },
                                    { metric: 'Expected Shortfall', value: '-7.8%' },
                                    { metric: 'Beta to Market', value: '1.12' },
                                    { metric: 'Tracking Error', value: '4.5%' }
                                ].map((item, index) => (_jsxs("div", { className: "flex justify-between items-center p-3 bg-gray-50 rounded-lg", children: [_jsx("span", { className: "text-gray-700", children: item.metric }), _jsx("span", { className: "font-semibold text-gray-900", children: item.value })] }, index))) })] }), _jsxs("div", { className: "bg-white rounded-xl shadow-sm border border-gray-200 p-6", children: [_jsx("h3", { className: "text-lg font-semibold text-gray-900 mb-4", children: "Performance Attribution" }), _jsx("div", { className: "space-y-3", children: [
                                    { factor: 'Stock Selection', contribution: '+3.2%' },
                                    { factor: 'Sector Allocation', contribution: '+1.8%' },
                                    { factor: 'Currency Effects', contribution: '-0.4%' },
                                    { factor: 'Transaction Costs', contribution: '-0.9%' }
                                ].map((item, index) => (_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-gray-600", children: item.factor }), _jsx("span", { className: `font-medium ${item.contribution.startsWith('+')
                                                ? 'text-green-600'
                                                : item.contribution.startsWith('-')
                                                    ? 'text-red-600'
                                                    : 'text-gray-600'}`, children: item.contribution })] }, index))) })] })] })] }));
};
