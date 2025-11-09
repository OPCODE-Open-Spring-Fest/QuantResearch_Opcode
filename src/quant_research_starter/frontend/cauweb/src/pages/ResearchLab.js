import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { LineChart, BarChart3, Activity } from 'lucide-react';
export const ResearchLab = () => {
    const factors = [
        { name: 'Momentum', description: 'Price momentum factors', icon: Activity, color: 'blue' },
        { name: 'Value', description: 'Valuation metrics', icon: BarChart3, color: 'green' },
        { name: 'Size', description: 'Market capitalization', icon: LineChart, color: 'purple' },
        { name: 'Volatility', description: 'Price volatility measures', icon: Activity, color: 'red' }
    ];
    return (_jsxs("div", { className: "p-8", children: [_jsxs("div", { className: "mb-8", children: [_jsx("h1", { className: "text-3xl font-bold text-gray-900", children: "Research Lab" }), _jsx("p", { className: "text-gray-600 mt-2", children: "Explore and analyze alpha factors" })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8", children: factors.map((factor, index) => {
                    const Icon = factor.icon;
                    const colorClasses = {
                        blue: 'bg-blue-100 text-blue-600',
                        green: 'bg-green-100 text-green-600',
                        purple: 'bg-purple-100 text-purple-600',
                        red: 'bg-red-100 text-red-600'
                    };
                    return (_jsxs("div", { className: "bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow", children: [_jsx("div", { className: `w-12 h-12 ${colorClasses[factor.color]} rounded-lg flex items-center justify-center mb-4`, children: _jsx(Icon, { className: "w-6 h-6" }) }), _jsx("h3", { className: "text-lg font-semibold text-gray-900 mb-2", children: factor.name }), _jsx("p", { className: "text-gray-600 text-sm", children: factor.description }), _jsx("button", { className: "mt-4 w-full bg-gray-100 text-gray-700 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm", children: "Analyze Factor" })] }, index));
                }) }), _jsxs("div", { className: "bg-white rounded-xl shadow-sm border border-gray-200 p-6", children: [_jsx("h3", { className: "text-lg font-semibold text-gray-900 mb-4", children: "Factor Performance" }), _jsx("div", { className: "h-96 bg-gray-100 rounded-lg flex items-center justify-center text-gray-500", children: "Factor performance charts will be displayed here" })] })] }));
};
